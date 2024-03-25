first = False
def check_config() -> int:
    import json
    import os
    
    if not os.path.exists("config.json"): return 1
    with open("config.json", encoding="utf-8") as config:
        json.load(config)
    return 0

def return_config() -> dict:
    global first
    import json
    import colorama
    from function.utils import logo
    
    colorama.init()
    COLOR = colorama.Fore

    while True:
        if first:
            logo()
            first = False
        match check_config():
            case 0:
                with open("config.json", encoding="utf-8") as config_file: return json.load(config_file)
                print(f"[{COLOR.GREEN}+{COLOR.RESET}] конфиг успешно загружен")
            case 1:
                create_config()
                input(f"[{COLOR.RED}-{COLOR.RESET}] конфиг не найден, он был пересоздан, настройте его и нажмите enter")
            case 2:
                create_config()
                input(f"[{COLOR.YELLOW}*{COLOR.RESET}] конфиг найден, но он повреждён, он был переименован в old_config.json и был создан новый, проверьте правильность json и перенесите настройки в новый json файл")
def create_config() -> None:
    import json
    import os

    config = {
        "zapros": ["zapros1", "zapros2"],
        "parse_zapros": False,
        "email_parse": True,
        "login_parse": True,
        "number_parse": True,
        "parse_full": False,
        "folder": "Result",
        "file_block": 128
    }
    json_config = json.dumps(config, indent=1)

    if not os.path.exists("config.json"):
        with open("config.json", mode="a+", encoding="utf-8") as config_file:
            config_file.write(json_config)
    elif os.path.exists("config.json"):
        os.rename("config.json", "old_config.json")
        with open("config.json", mode="a+", encoding="utf-8") as config_file:
            config_file.write(json_config)

def get_path() -> list:
    import os
    import function.utils as utils
    import colorama
    import ctypes

    colorama.init()
    COLOR = colorama.Fore
    
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW("Работает drag&drop")
        utils.logo()
        base = input('[Для выхода из скрипта напишите exit]\n[Path]=> ').replace('"', '').replace("& '", '').replace("'", '')
        if os.path.exists(base):
            if os.path.isfile(base): return [True, base]
            if os.path.isdir(base): return [False, base]
        if base.lower() == 'exit': exit()
        input(f'[{COLOR.YELLOW}*{COLOR.RESET}] путь до {base} не найден, проверьте правильность пути и попробуйте снова')

def reading(file: str) -> list:
    import mmap

    all_find: int = 0
    all_lines: int = 0

    config = return_config()

    with open(file=file, mode='r', encoding="utf-8", errors="ignore") as file_read:
        with mmap.mmap(file_read.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_read:
            while True:
                chunk = mmap_read.read(config["file_block"] * 1024 * 1024)
                if not chunk: return [all_find, all_lines]
                result = read_chunk(config=config, chunk=chunk)
                all_find += result[0]
                all_lines += result[1]

def read_chunk(config: dict, chunk: list) -> list:
    import function.text_utils as text_utils
    import regex

    Dict = {}

    bad_list: list = ["unknown", "none", "*"]
    repl_list: list = [";", " ", "|", ","]

    email_regex = regex.compile(r"^\S+@\S+\.\S+$")
    login_regex = regex.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
    number_regex = regex.compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")
    
    chunk = chunk.decode().split("\r\n")
    all_len = len(chunk)
    for _, line in enumerate(chunk):
        if config["parse_zapros"]:
            for _, zapros in enumerate(config["zapros"]):
                if zapros in line:
                    result = text_utils.main(line=line, bad_list=bad_list, repl_list=repl_list, email=email_regex, login=login_regex, number=number_regex, config=config)
                    if result[0]:
                        Dict.setdefault(f"{zapros}_{result[1]}", set()).add(f"{result[3]}:{result[4]}")
                        if config["parse_full"]:
                            Dict.setdefault(f"{zapros}_{result[1]}_full", set()).add(f"{result[2]}{result[3]}:{result[4]}")
        else:
            result = text_utils.main(line=line, bad_list=bad_list, repl_list=repl_list, email=email_regex, login=login_regex, number=number_regex, config=config)
            if result[0]:
                Dict.setdefault(result[1], set()).add(f"{result[3]}:{result[4]}")
                if config["parse_full"]:
                    Dict.setdefault(f"{result[1]}_full", set()).add(f"{result[2]}{result[3]}:{result[4]}")
    return [write(Dict=Dict, file_path=config["folder"]), all_len]

def return_count(Dict: dict) -> int:
    count: int = 0
    for key, value in Dict.items():
        if "_full" not in key:
            count += len(value)
    return count

def write(Dict: dict, file_path: str) -> int:
    import os

    if not os.path.exists(file_path): os.mkdir(file_path)

    count = return_count(Dict=Dict)
    for key, value in Dict.items():
        if value:
            with open(f"{file_path}/{key}.txt", mode="a+", encoding="utf-8", errors="ignore") as file:
                for _, line in enumerate(value):
                    file.write(f"{line}\n")
    return count

def main(path: list) -> None:
    import os
    import function.utils as utils
    utils.logo()
    if path[0] and path[1].endswith(".txt"):
        find, all = reading(path[1])
        print(f"Обработал файл: {path[1]} | нашёл строк: {find} | Всего строк в файле: {all}")
    else:
        for root, _, files in os.walk(path[1]):
            for file in files:
                if file.endswith(".txt"):
                    find, all = reading(f"{root}/{file}")
                    print(f"Обработал файл: {path[1]} | нашёл строк: {find} | Всего строк в файле: {all}")