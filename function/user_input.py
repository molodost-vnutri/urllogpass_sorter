def get_path() -> list:
    import os
    from function.utils import logo
    import colorama
    import ctypes

    colorama.init()
    COLOR = colorama.Fore

    while True:
        ctypes.windll.kernel32.SetConsoleTitleW("Работает drag&drop")
        logo()
        base = input('[Для выхода из скрипта напишите exit]\n[Path]=> ').replace('"', '').replace("& '", '').replace("'", '')
        if os.path.exists(base):
            if os.path.exists(base): return return_files(base)
        if base.lower() == 'exit': exit()
        input(f'[{COLOR.YELLOW}*{COLOR.RESET}] путь до {base} не найден, проверьте правильность пути и попробуйте снова')

def return_files(base: str) -> list:
    import os

    paths: list = []

    if os.path.isfile(base): return [base]
    if os.path.isdir(base):
        for root, _, files in os.walk(base):
            for path in files:
                file = f"{root}\{path}"
                if file.endswith(".txt") and os.path.isfile(file):
                    paths.append(file)
    return paths