from datetime import datetime
from os import walk, makedirs
from os.path import exists, getsize, isdir, isfile, join

from colorama import Fore, init
from ctypes import windll

from modules.json_module import JsonLoad
from modules.logo import logo
from modules.shemas import SConfig

init()

time = datetime.now().strftime("%Y-%m-%d")

config: SConfig = JsonLoad().config

class FileIo:
    def __init__(self, path: str):
        self.path: str = path
        self.small: bool = True if int(getsize(path) / 1024) else False
    
    def yield_file_read(self):
        with open(
            file=self.path,
            mode='r',
            encoding='utf-8',
            errors='ignore'
        ) as file:
            if self.small:
                yield list(set(line.strip() for line in file.readlines()))
            while True:
                chunk = file.readlines(500000)
                if not chunk: break
                yield chunk

class FolderSearch:
    def __init__(self, path: str):
        self.files = []
        if isfile(path):
            self.files.append(path)
        else:
            for root, _, files in walk(path):
                self.files.extend([join(root, file) for file in files if file.endswith('.txt')])

def write_results(results: dict):
    folder = join(config.folder, time)
    if not isdir(folder):
        makedirs(folder)
    for key, value in results.items():
        if value:
            with open(file=join(folder, key+'.txt'),
                      mode='a',
                      encoding='utf-8',
                      errors='ignore') as file:
                for line in value:
                    file.write(line+'\n')

def get_path() -> str:
    while True:
        print(logo)
        windll.kernel32.SetConsoleTitleW("Работает drag&drop")
        base = input('[Для выхода из скрипта напишите exit]\n[Path]=> ').replace('"', '').replace("& '", '').replace("'", '')
        if exists(base):
            return base
        if base.lower() == 'exit': exit()
        input(f'[{Fore.YELLOW}*{Fore.RESET}] путь до {base} не найден, проверьте правильность пути и попробуйте снова')
def load_settings(path: str) -> list[str]:
    if not isfile(path):
        with open(
            file=path,
            mode='a',
            encoding="utf-8",
        ) as file:
            if path == "zapros.txt":
                file.writelines([line+'\n' for line in ['zapros1', 'zapros2']])
            if path == "bad_list.txt":
                file.writelines([line+'\n' for line in ['unknown', 'null']])
            if path == "repl_list.txt":
                file.writelines([line+'\n' for line in [';', '|', ' ']])
    with open(
        file=path,
        mode='r',
        encoding="utf-8"
    ) as file:
        return [line.strip().lower() for line in file if line.strip()]

zapros_list = load_settings('zapros.txt')
bad_list = load_settings('bad_list.txt')