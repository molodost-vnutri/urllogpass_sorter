from multiprocessing import Pool
from typing import Optional

from modules.cpu import logical_core
from modules.file import config, zapros_list
from modules.text import Text
from modules.submodules import SUlp


def worker_function(chunk: list[str]) -> dict[str, set[str]]:
    processor = ChunkProcessor(chunk)
    return processor.__read_chunk__(chunk)

class ChunkProcessor:
    def __init__(self, chunk: list[str]):
        self.chunk = chunk

    def __chunkify__(self):
        chunk_len = len(self.chunk)
        if chunk_len == 0:
            return
        chunk_size = max(1, chunk_len // logical_core)
        for i in range(0, chunk_len, chunk_size):
            yield self.chunk[i:i + chunk_size]

    def process(self):
        chunks = list(self.__chunkify__())
        
        with Pool(processes=min(logical_core, len(chunks))) as pool:
            results = pool.map(worker_function, chunks)
        
        final_result: dict[str, set[str]] = {}
        find: int = 0
        
        for result_line in results:
            for key, value in result_line.items():
                if not str(key).endswith('full'):
                    find += len(value)
                if key not in final_result:
                    final_result[key] = set()
                final_result[key].update(value)
        
        return [final_result, find]

    def __add_result__(self, result_line: dict[str, set[str]], result: Optional[SUlp], zapros: str = ''):
        if result:
            result_key = f'{zapros + "_" if zapros else ""}{result.typedata}'
            
            result_line.setdefault(result_key, set()).add(result.credit)
            if config.parse_full:
                result_full_key = f'{result_key}_{result.typeulp}'
                result_line.setdefault(result_full_key, set()).add(result.full)

    def __read_chunk__(self, chunk: list[str]) -> dict[str, set[str]]:
        result_line: dict[str, set[str]] = {}
        if config.parse_zapros:
            for line in chunk:
                for zapros in zapros_list:
                    if zapros in line.lower():
                        result = Text(line).result
                        self.__add_result__(result_line=result_line, result=result, zapros=zapros)
        else:
            for line in chunk:
                result = Text(line).result
                self.__add_result__(result_line=result_line, result=result)
        return result_line
