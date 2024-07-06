import os
import json
from typing import Union

from modules.shemas import SJson


class JsonLoad(SJson):
    @staticmethod
    def __create_config__():
        if not os.path.isfile('config.json'):
            config = {
                "zapros": ["zapros", "zapros"],
                
                "parse_zapros": False,
                
                "parse_email": True,
                "parse_login": True,
                "parse_number": True,

                "parse_full": True,
                "bad_list": ["unknown", "none"],
                "thread_auto": True,
                "threads": 4,
                "buffer": 10000,
                "folder": "Result"
            }
            config_json = json.dumps(config, indent=2)
            with open("config.json", "+a", encoding="utf-8") as config_file:
                config_file.write(config_json)
    
    @classmethod
    def get(cls) -> Union[Exception, SJson]:
        try:
            cls.__create_config__()
            with open('config.json', encoding='utf-8') as config_file:
                jsonbody = json.load(config_file)
                return SJson(**jsonbody)
        except Exception as e:
            return e