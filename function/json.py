def check_config() -> int:
    import json
    import os

    if not os.path.exists("config.json"): return 1
    try:
        with open("config.json", encoding="utf-8") as config_file:
            json.load(config_file)
            return 0
    except:
        return 2

def return_config(first: bool) -> dict:
    import json
    import colorama
    from function.utils import logo

    colorama.init()
    COLOR = colorama.Fore

    while True:
        if first:
            logo()
        match check_config():
            case 0:
                if first:
                    print(f"[{COLOR.GREEN}+{COLOR.RESET}] конфиг успешно загружен")
                with open("config.json", encoding="utf-8") as config_file: return json.load(config_file)
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

        "check_regex": True,
        "check_len": True,

        "email_len": [8, 25],
        "login_len": [5, 25],
        "number_len": [11, 16],
        "password_len": [8, 25],


        "buffer_count": 10000,
        "folder": "Result",
    }
    json_config = json.dumps(config, indent=1)

    if not os.path.exists("config.json"):
        with open("config.json", mode="a+", encoding="utf-8") as config_file:
            config_file.write(json_config)
    elif os.path.exists("config.json"):
        os.rename("config.json", "old_config.json")
        with open("config.json", mode="a+", encoding="utf-8") as config_file:
            config_file.write(json_config)
