first = True
def check_config() -> int:
    import os
    import json

    if not os.path.exists('config.json'):
        create_config()
        return 2
    try:
        with open('config.json', mode='r', encoding='utf-8') as config_file:
            json.load(config_file)
        return 0
    except:
        os.rename('config.json', 'old_config.json') if not os.path.exists('old_config.json') else os.remove('old_config.json') | os.rename('config.json', 'old_config.json')
        create_config()
        return 1

def create_config() -> None:
    import json

    config = {
            'zapros': ['zapros', 'zapros'],
            'parse_zapros': False,
            'email_parse': True,
            'login_parse': True,
            'number_parse': True,
            'parse_full': False,
            'folder': 'Result',
            'file_block': 128,
            'log': False
    }
    with open('config.json', mode='a') as config_file:
        config_file.write(json.dumps(config, indent=1))

def return_config(first: bool) -> {}:
    import json
    import utils
    import colorama
    import ctypes

    ctypes.windll.kernel32.SetConsoleTitleW("URL сортер")

    colorama.init()
    COLOR = colorama.Fore

    status = None
    while status != 0:
        if first:
            utils.logo()
            status = check_config()
            if status == 0:
                print(f'[{COLOR.GREEN}+{COLOR.RESET}] конфиг успешно загружен')
                with open('config.json', encoding='utf-8') as config_file:
                    return json.load(config_file)
            if status == 1:
                input(f'[{COLOR.YELLOW}*{COLOR.RESET}] конфиг повреждён он был переименован в old_config.json, перенесите настройки в новый конфиг и нажмите enter')
            if status == 2:
                input(f'[{COLOR.RED}-{COLOR.RESET}] конфиг не найден, он был создан, настройте его и найжмите enter')
        else:
            with open('config.json', encoding='utf-8') as config_file:
                return json.load(config_file)

def get_path() -> str:
    import os
    import utils
    import colorama
    import ctypes

    colorama.init()
    COLOR = colorama.Fore
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW("Работает drag&drop")
        utils.logo()
        base = input('[Для выхода из скрипта напишите exit]\n[Path]=> ').replace('"', '').replace("& '", '').replace("'", '')
        if os.path.exists(base): return base
        if base.lower() == 'exit': exit()
        input(f'[{COLOR.YELLOW}*{COLOR.RESET}] путь до {base} не найден, проверьте правильность пути и попробуйте снова')

def read_file(file: str):
    import mmap

    config = return_config(False)
    folder_path = create_folder(config=config)
    
    config['folder_path'] = folder_path
    mass = {}
    first = True
    with open(file=file, mode='r', encoding='utf-8', errors='ignore') as file_read:
        with mmap.mmap(file_read.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_read:
            while True:
                chunk = mmap_read.read(config['file_block'] * 1024 * 1024)
                if not chunk: return [mass, config]
                result = read_chunk(config=config, chunk=chunk)
                mass = result if first else mass
                for key, items in result.items():
                    try: mass[key] += items
                    except: mass[key] = items
                first = False

def read_chunk(config: {}, chunk: []) -> [int, int, int]:
    import text_utils

    Dict = {}
    for index, line in enumerate(chunk.decode().split('\r\n')):
        if config['parse_zapros']:
            for index, zapros in enumerate(config['zapros']):
                if zapros in line:
                    if line.count(':') > 1:
                        data, password = line.split(':')[-2:]
                        data, password = data.replace(' ', ''), password.replace(' ', '')
                        match text_utils.regex_check(data=data, password=password, config=config):
                            case 'email':
                                Dict.setdefault(f'{zapros}_email', set()).add(f'{data}:{password}')
                                if config['parse_full']:
                                    Dict.setdefault(f'{zapros}_email_full', set()).add(line)
                            case 'login':
                                Dict.setdefault(f'{zapros}_login', set()).add(f'{data}:{password}')
                                if config['parse_full']:
                                    Dict.setdefault(f'{zapros}_login_full', set()).add(line)
                            case 'number':
                                Dict.setdefault(f'{zapros}_number', set()).add(f'{data}:{password}')
                                if config['parse_full']:
                                    Dict.setdefault(f'{zapros}_number_full', set()).add(line)
        else:
            if ':' in line:
                data, password = line.split(':')[-2:]
                match text_utils.regex_check(data=data, password=password, config=config):
                    case 'email':
                        Dict.setdefault('email', set()).add(f'{data}:{password}')
                    case 'login':
                        Dict.setdefault('login', set()).add(f'{data}:{password}')
                    case 'number':
                        Dict.setdefault('number', set()).add(f'{data}:{password}')
    write(Dict=Dict, file_path=config['folder_path'])
    return return_count(Dict=Dict)

def return_count(Dict: {}):
    Dict_count: {} = {}
    for key, value in Dict.items():
        if '_full' not in key:
            Dict_count[key] = len(value)
    return Dict_count

def write(Dict: {}, file_path) -> None:
    for key, value in Dict.items():
        if value:
            with open(f'{file_path}/{key}.txt', mode='a+', encoding='utf-8') as file:
                for line in value:
                    file.write(f'{line}\n')

def create_folder(config: {}) -> str:
    import os
    import datetime

    time = datetime.datetime.now().strftime("%Y_%m_%d")

    os.mkdir(config['folder']) if not os.path.exists(config['folder']) else None
    os.mkdir(f'{config["folder"]}/{time}') if not os.path.exists(f'{config["folder"]}/{time}') else None
    return f'{config["folder"]}/{time}'

def working(path_data) -> [int, int, int]:
    import os
    import colorama

    colorama.init()
    COLOR = colorama.Fore

    config = return_config(True)
    if os.path.isfile(path_data):
        result = f'[{COLOR.GREEN}+{COLOR.RESET}] {path_data}: '
        result_in_log = f'[+] {path_data}: '
        db, configure = read_file(path_data)
        for num, value in db.items():
            result += f'{COLOR.BLUE}{num.replace("_", " ")} {COLOR.GREEN}{value}{COLOR.RESET} | {COLOR.BLUE}Вес {COLOR.GREEN}{round(os.stat(path_data).st_size / (1024 * 1024))}mb{COLOR.RESET} | '
            result_in_log += f'{num.replace("_", " ")} {value} | Вес {round(os.stat(path_data).st_size / (1024 * 1024))}mb | '
        print(result[:-2])
        if config['log']:
            write_log(result=result_in_log, configure=configure)
    if os.path.isdir(path_data):
        for root, dirs, files in os.walk(path_data):
            for file in files:
                result_in_log = f'[+] {os.path.join(root, file)}: '
                result = f'[{COLOR.GREEN}+{COLOR.RESET}] {os.path.join(root, file)}: '
                if file.endswith('.txt'):
                    db, configure = read_file(os.path.join(root, file))
                    for num, value in db.items():
                        result_in_log += f'{num.replace("_", " ")} {value} | Вес {round(os.stat(os.path.join(root, file)).st_size / (1024 * 1024))}mb | '
                        result += f'{COLOR.BLUE}{num.replace("_", " ")} {COLOR.GREEN}{value}{COLOR.RESET} | Вес {COLOR.GREEN}{round(os.stat(os.path.join(root, file)).st_size / (1024 * 1024))}mb{COLOR.RESET} | '
                    print(result[:-2])
                    if config['log']:
                        write_log(result=result_in_log, configure=configure)

def write_log(result: str, configure: {}):
    global first

    import os

    if not os.path.exists('LOGS'): os.mkdir('LOGS')
    file = f'LOGS/{configure["folder_path"].split("/")[-1]}.txt'
    with open(file, 'a+', encoding='utf-8') as log_file:
        if first:
            first = False
            log_file.write("Настройки сессии:\n")
            for key, value in configure.items():
                log_file.write(f'{key}: {value}\n')
            log_file.write('\n\n')
        if not first: log_file.write(f'{result}\n\n')