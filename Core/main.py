from pathlib import Path

from Core.Threads import ThreadsSpawner
from Core.schemes import SResultMain
from Core.config import config
from Core.writer import write_results

def run(path: Path) -> SResultMain:
    chunk: list[str] = []
    result = SResultMain()
    with open(path, encoding='utf-8', errors='ignore') as  file:
        for line in file:
            chunk.append(line)
            if len(chunk) >= config.count_line_in_buffer:
                process_chunk(chunk, result)
                chunk.clear()
        
        if chunk:
            process_chunk(chunk, result)

    return result

def process_chunk(chunk: list[str], result: SResultMain) -> None:
    data = ThreadsSpawner(chunk).process()
    result.append_result(data)
    write_results(data.result)