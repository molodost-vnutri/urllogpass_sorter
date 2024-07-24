from json import dumps, load
from os.path import isfile

from modules.shemas import SConfig

class JsonLoad:
    def __init__(self) -> None:
        self.__check_exist__()
        self.__get__()
    def __check_exist__(self):
        if not isfile('config.json'):
            config = {
                "parse_zapros": False,
                "parse_email": True,
                "parse_login": True,
                "parse_number": True,
                "parse_full": False,
                "email_len": [8, 25],
                "login_len": [5, 25],
                "number_len": [11, 16],
                "password_len": [8, 25],
                "thread_auto": True,
                "threads": 4,
                "folder": "Result"
            }
            with open(
                file="config.json",
                mode='a',
                encoding="utf-8"
            ) as config_file:
                config_file.write(dumps(config, indent=2))
    def __get__(self):
        with open(
            file="config.json",
            mode='r',
            encoding="utf-8",
        ) as config_file:
            self.config = SConfig(**load(config_file))
