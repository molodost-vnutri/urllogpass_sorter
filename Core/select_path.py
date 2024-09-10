from pathlib import Path
from ctypes import windll

from colorama import Fore

from Core.system import clear_screen
from Core.logo import logo

def get_current_path() -> Path:
    '''
    Получение пути от пользователя
    '''

    while True:
        clear_screen()
        logo()
        windll.kernel32.SetConsoleTitleW("Работает Drag&drop")
        path_string = input('[Для выхода напишите exit]\n[Path]=> ').replace('"', '').replace("& '", '').replace("'", '')
        path = Path(path_string)
        if path.exists():
            windll.kernel32.SetConsoleTitleW("")
            return path
        if path_string.lower() == 'exit':
            exit()

        input(f'[{Fore.YELLOW}*{Fore.RESET}] path {path_string} does not exist, check the path and try again')
