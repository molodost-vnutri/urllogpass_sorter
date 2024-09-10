from multiprocessing import Pool
from typing import Optional

from Core.settings import init_threads_count
from Core.config import config, zapros_list
from Core.unzip_line import Unzip
from Core.schemes import SResultSpawner, SResultUlp


def worker_function(chunk: list[str]) -> dict[str, set[str]]:
    spawner = ThreadsSpawner(chunk)
    return spawner.reading_chunk(chunk)

class ThreadsSpawner:
    chunk: list[str]
    chunk_length: int
    threads: int = init_threads_count()

    def chunkify(self):
        chunk_size = max(1, self.chunk_length // self.threads)
        for i in range(0, self.chunk_length, chunk_size):
            yield self.chunk[i:i + chunk_size]
    
    def process(self) -> SResultSpawner:
        chunks = list(self.chunkify())
        with Pool(processes=min(self.threads, len(chunks))) as pool:
            results = pool.map(worker_function, chunks)
        
        return SResultSpawner(results)

    def reading_chunk(self, chunk: list[str]) -> dict[str, set[str]]:
        results: dict[str, set[str]] = {}
        for line in chunk:
            line_lower = line.lower().strip()

            if config.parse_zapros:
                for zapros in zapros_list:
                    if zapros in line_lower:
                        result = Unzip.get_result(line_lower)
                        self.add_result_in_dict(results, result, zapros)
            else:
                result = Unzip.get_result(line_lower)
                self.add_result_in_dict(results, result)
        return results
    
    def add_result_in_dict(self, results: dict[str, set[str]], result: Optional[SResultUlp], zapros: str = ''):
        if result:
            result_key = f'{zapros + "_" if zapros else ""}{result.datatype}'
            results.setdefault(result_key, set()).add(result.credits)
            if config.parse_full:
                result_full_key = f'{result_key}_{result.linetype}_full'
                results.setdefault(result_full_key, set()).add(result.urllogpass)
    
    def __init__(self, chunk: list[str]):
        self.chunk = chunk
        self.chunk_length = len(chunk)
