def read_paths(paths: list):
    import ctypes
    import colorama
    from function.utils import converter, logo

    colorama.init()
    COLOR = colorama.Fore

    logo()

    all_find = 0
    lines = 0

    checked: int = 0

    ctypes.windll.kernel32.SetConsoleTitleW(f"Нашёл {len(paths)} файлов, начинаю работу")

    for file in paths:
        find, line = read_file(file=file)
        print(f"[{COLOR.GREEN}+{COLOR.RESET}] Прочекал файл {file} нашёл {find} строк, всего строк {line}")
        all_find += find
        lines += line
        checked += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"Прочекано [{checked}/{len(paths)}] файлов, найдено/всего строк [{converter(all_find)}/{converter(lines)}]")

def create_folder(config: dict) -> str:
    import datetime
    import os

    current_date = datetime.date.today().isoformat()

    if not os.path.exists(config["folder"]):
        os.mkdir(config["folder"])
    if not os.path.exists(f'{config["folder"]}/{current_date}'):
        os.mkdir(f'{config["folder"]}/{current_date}')
    return f'{config["folder"]}/{current_date}'

def read_file(file: str) -> list:
    import regex
    from function.text import main
    from function.json import return_config
    from function.utils import check_buffer

    all_lines: int = 0
    all_find: int = 0

    database: dict = {}

    config = return_config(False)
    folder = create_folder(config=config)

    bad_list: list = ["unknown", "none", "*"]
    repl_list: list = [";", " ", "|", ","]

    email_regex = regex.compile(r"^\S+@\S+\.\S+$")
    login_regex = regex.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
    number_regex = regex.compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")
    

    with open(file, encoding="utf-8", errors="ignore") as file_read:
        if config["parse_zapros"]:
            for index, line in enumerate(file_read):
                line = line.strip()
                if check_buffer(database=database, config=config):
                    all_find += write_result(database=database, folder=folder)
                    database.clear()
                all_lines = index
                status = check_zapros(line=line, config=config)
                if status is not None:
                    result = main(line=line, bad_list=bad_list, repl_list=repl_list, email_regex=email_regex, login_regex=login_regex, number_regex=number_regex, config=config)
                    if result is not None:
                        url, data, password, type_data = result
                        match type_data:
                            case 0:
                                database.setdefault(f"{status}_email", set()).add(f"{data}:{password}")
                                if config["parse_full"]:
                                    database.setdefault(f"{status}_email_full", set()).add(f"{url}:{data}:{password}")
                            case 1:
                                database.setdefault(f"{status}_login", set()).add(f"{data}:{password}")
                                if config["parse_full"]:
                                    database.setdefault(f"{status}_login_full", set()).add(f"{url}:{data}:{password}")
                            case 2:
                                database.setdefault(f"{status}_number", set()).add(f"{data}:{password}")
                                if config["parse_full"]:
                                    database.setdefault(f"{status}_number_full", set()).add(f"{url}:{data}:{password}")
                            case 3:
                                database.setdefault(f"{status}_all_datas", set()).add(f"{data}:{password}")
                                if config["parse_full"]:
                                    database.setdefault(f"{status}_all_datas_full", set()).add(f"{url}:{data}:{password}")

        if not config["parse_zapros"]:
            for index, line in enumerate(file_read):
                line = line.strip()
                if check_buffer(database=database, config=config):
                    all_find += write_result(database=database, folder=folder)
                    database.clear()
                all_lines = index
                result = main(line=line, bad_list=bad_list, repl_list=repl_list, email_regex=email_regex, login_regex=login_regex, number_regex=number_regex, config=config)
                if result is not None:
                    url, data, password, type_data = result
                    match type_data:
                        case 0:
                            database.setdefault("email", set()).add(f"{data}:{password}")
                            if config["parse_full"]:
                                database.setdefault("email_full", set()).add(f"{url}:{data}:{password}")
                        case 1:
                            database.setdefault("login", set()).add(f"{data}:{password}")
                            if config["parse_full"]:
                                database.setdefault("login_full", set()).add(f"{url}:{data}:{password}")
                        case 2:
                            database.setdefault("number", set()).add(f"{data}:{password}")
                            if config["parse_full"]:
                                database.setdefault("number_full", set()).add(f"{url}:{data}:{password}")
                        case 3:
                            database.setdefault("all_datas", set()).add(f"{data}:{password}")
                            if config["parse_full"]:
                                database.setdefault("all_datas_full", set()).add(f"{url}:{data}:{password}")
    all_find += write_result(database=database, folder=folder)
    return [all_find, all_lines]

def write_result(database: dict, folder: str) -> int:
    count: int = 0
    for key, dict in database.items():
        if len(dict) != 0:
            with open(f"{folder}/{key}.txt", mode="+a", encoding="utf-8", errors="ignore") as result:
                for _, line in enumerate(dict):
                    result.write(line + "\n")
        if not str(key).endswith("_full"):
            count += len(dict)
    return count

def check_zapros(line: str, config: dict) -> str or None: # type: ignore
    line = line.lower()
    for _, zapros in enumerate(config["zapros"]):
        if zapros in line:
            return zapros
    return None