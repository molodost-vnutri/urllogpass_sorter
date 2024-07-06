import concurrent.futures
import os
from typing import Union, Optional
from datetime import datetime

from modules.shemas import SFileResult, SJson, SUlp
from modules.text import Text
from modules.json import JsonLoad
from modules.config_cpu import ConfigCpu

class ChunkProcessor:
    def __init__(self, chunk: list[str], config: SJson, threads: int):
        self.chunks: list[str] = chunk
        self.config: SJson = config
        self.threads: int = threads
    
    def __chunkify__(self):
        chunk_size = len(self.chunks) // self.threads
        for i in range(0, len(self.chunks), chunk_size):
            yield self.chunks[i:i + chunk_size]
    
    def __read_chunk__(self, chunk: list[str]):
        result_lines: dict = {}
        if self.config.parse_zapros:
            for _, line in enumerate(chunk):
                for _, zapros in enumerate(self.config.zapros):
                    if zapros in line.lower():
                        result: Optional[SUlp] = Text(ulp=line, config=self.config).get()
                        if result is not None:
                            result_lines.setdefault(f'{zapros}_{result.typedata}', set()).add(result.extract_credit())
                            if self.config.parse_full:
                                result_lines.setdefault(f'{zapros}_{result.typedata}_{result.typeulp}_full', set()).add(result.extract_full_line())
        else:
            for _, line in enumerate(chunk):
                result: Optional[SUlp] = Text(ulp=line, config=self.config).get()
                if result is not None:
                    result_lines.setdefault(f'{result.typedata}', set()).add(result.extract_credit())
                    if self.config.parse_full:
                        result_lines.setdefault(f'{result.typedata}_{result.typeulp}_full', set()).add(result.extract_full_line())
        return result_lines
    
    def process(self):
        chunks = list(self.__chunkify__())
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            results = list(executor.map(self.__read_chunk__, chunks))
        finalresult: dict = {}
        find: int = 0
        for key, value in results[0].items():
            if not str(key).endswith('full'):
                find += len(value)
            if key not in finalresult and value:
                finalresult[key] = set()
            if value: finalresult[key].update(value)
        return [finalresult, find]

class FileExtractor:
    def __init__(self, path: str):
        self.path: str = path
        self.config: SJson = JsonLoad.get()
        self.threads: int = ConfigCpu(thread_auto=self.config.thread_auto, threads=self.config.threads).get()
        self.files: list[str] = FileFinder(path=self.path, config=self.config).get()
        self.buffer: list[str] = []
        self.results: list[SFileResult] = []
        self.result: SFileResult
        self.datetime = datetime.now().strftime('%Y-%m-%d')
    
    def reading(self):
        for _, file in enumerate(self.files):
            self.result = SFileResult(path=file)
            with open(file, encoding='utf-8', errors='ignore') as filebody:
                for line in filebody:
                    self.buffer.append(line.strip())
                    if len(self.buffer) >= 10000:
                        self.result.all_lines += len(self.buffer)
                        result, find = ChunkProcessor(self.buffer, config=self.config, threads=self.threads).process()
                        self.result.find += find
                        self.__write_results__(result)
                        self.buffer.clear()
                        
            if self.buffer:
                self.result.all_lines += len(self.buffer)
                result, find = ChunkProcessor(self.buffer, config=self.config, threads=self.threads).process()
                self.result.find += find
                self.__write_results__(result)
                self.buffer.clear()
        self.results.append(self.result)

        return self.results
    def __write_results__(self, result: dict[str, set]):
        if not os.path.isdir(self.config.folder):
            os.mkdir(self.config.folder)
        if not os.path.isdir(f'{self.config.folder}/{self.datetime}'):
            os.mkdir(f'{self.config.folder}/{self.datetime}')
        for key, value in result.items():
            with open(f'{self.config.folder}/{self.datetime}/{key}.txt', mode='a+', encoding='utf-8') as result_file:
                for res in value:
                    result_file.write(f'{res}\n')

class FileFinder:
    def __init__(self, path: str, config: SJson):
        self.path: str = path
        self.files: list[str] = []
        self.config: SJson = config

    def get(self) -> Union[list[None], list[str]]:
        if os.path.isfile(self.path):
            self.files.append(self.path)
            return self.files
        for root, dirs, files in os.walk(self.path):
            if self.config.folder in dirs:
                continue
            for file in files:
                path = f'{root}/{file}'
                if path.endswith('.txt'):
                    self.files.append(path)
        return self.files