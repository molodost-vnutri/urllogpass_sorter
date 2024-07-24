from typing import Optional

from colorama import Fore, init

from modules.file import FileIo, FolderSearch, write_results, get_path, zapros_list, bad_list
from modules.Threads import ChunkProcessor

init()

isgui = True


class Application:
    def __init__(self, path) -> Optional[list[str]]:
        self.files = FolderSearch(path).files
    def run(self):
        result: list[str] = []
        for file in self.files:
            find = 0
            for chunk in FileIo(file).yield_file_read():
                results = ChunkProcessor(chunk).process()
                write_results(results[0])
                find += results[1]
            if isgui:
                result.append(f'Обработал файл: {file}\n    нашёл {find} строк')
            if not isgui:
                print(f'[{Fore.GREEN}+{Fore.RESET}] Обработал файл: {file} | нашёл {find} строк')
        if isgui:
            return result

if __name__ == "__main__":
    isgui = False
    path = get_path()
    Application(path).run()
    input()