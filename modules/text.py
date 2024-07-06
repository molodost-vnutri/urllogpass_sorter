from urllib.parse import urlparse
from functools import lru_cache
from typing import Optional

from modules.shemas import SText, SJson, SUlp

bad_list_in_login: list[str] = ["(", ")", "*", "$", "!", "%", "&", "^", "#", "<", ">", "?", ":", ";", "~", "=", "[", "]"]
repl_list: list[str] = [";", " ", "|", ","]
config_len: dict = {
    "email_min": 8,
    "email_max": 25,
    "login_min": 5,
    "login_max": 25,
    "number_min": 11,
    "number_max": 16,
    "password_min": 8,
    "password_max": 25
}

class Text(SText):
    def __init__(self, ulp: str, config: SJson):
        self.ulp: str = ulp
        self.config: SJson = config
    def __get_credit__(self):
        if not self.valid:
            return
        for _, char in enumerate(repl_list):
            if char in self.ulp:
                self.ulp = self.ulp.replace(char, ":")
        
        if not self.ulp.count(":") in [2, 3, 4, 5]:
            self.valid = False
            return
        
        if self.ulp.startswith("http"): self.typeulp = 0
        elif self.ulp.startswith("android://"): self.typeulp = 1
        elif self.ulp.count("http") == 1 and self.ulp.count("://") == 1: self.typeulp = 2
        else:
            self.typeulp = 0
            self.ulp = 'https://'+self.ulp
    
        parts = self.ulp.split(":")

        if self.typeulp == 2:
            self.login = parts.pop(0)
            self.password = parts.pop(0)
            url = ":".join(parts)

            del parts
            
            try:
                host = urlparse(url)
                if host.hostname is not None:
                    self.url = host.hostname
                    if host.port is not None:
                        self.port = host.port
                    return
                self.valid = False
                return
            except:
                self.valid = False
                return

        self.password = parts.pop(-1)
        self.login = parts.pop(-1)
        url = ":".join(parts)

        del parts

        if self.typedata != 1:
            try:
                host = urlparse(url)
                if host.hostname is not None:
                    self.url = host.hostname
                    if host.port is not None:
                        self.port = host.port
                    return
                self.valid = False
                return
            except:
                self.valid = False
                return
    def __bad_word__(self):
        if any(bad in self.ulp for _, bad in enumerate(self.config.bad_list)):
            self.valid = False
            return
    def __check_len__(self):
        if not self.valid:
            return
        if len(self.password) > config_len["password_max"]:
            self.valid = False
            return
        
        match self.typedata:
            case 0:
                if self.config.parse_email:
                    if len(self.login) > config_len["email_max"]:
                        self.valid = False
                        return
            case 1:
                if self.config.parse_login:
                    if len(self.login) > config_len["login_max"]:
                        self.valid = False
                        return
            case 2:
                if self.config.parse_number:
                    if len(self.login) > config_len["number_max"]:
                        self.valid = False
                        return
            case _:
                self.valid = False
                return
    def __find_type__(self):
        if not self.valid:
            return

        if any(bad in self.login for _, bad in enumerate(bad_list_in_login)):
            self.valid = False
            return

        if not self.password.isascii() or not self.login.isascii() or len(self.password) < config_len["password_min"]:
            self.valid = False
            return
        if self.login.count('@') == 1:
            if self.config.parse_email:
                if len(self.login) < config_len["email_min"]:
                    self.valid = False
                    return
                login, domain = self.login.split('@')
                if len(login) == 1:
                    self.valid = False
                    return
                if 3 < domain.count('.') < 1:
                    self.valid == False
                    return
                self.typedata = 0
        else:
            if self.config.parse_number:
                num_list: list[int] = []
                for _, char in enumerate(list(self.login)):
                    try:
                        num_list.append(int(char))
                    except:
                        pass
                if len(num_list) > 0:
                    number: str = ''
                    for _, num in enumerate(num_list):
                        number = number + str(num)
                    if number[0] != 0 and len(number) >= config_len["number_min"]:
                        self.typedata = 2
                        return
            if self.config.parse_login:
                if not self.login.isascii():
                    self.valid = False
                    return
                if len(self.login) < config_len["login_min"]:
                    self.valid = False
                    return
                self.typedata = 1 
    @lru_cache()
    def get(self) -> Optional[SUlp]:
        self.__bad_word__()
        self.__get_credit__()
        self.__find_type__()
        self.__check_len__()
        if self.valid:
            if self.typedata != 1:
                self.typedata = 0
            return SUlp(typeulp=self.typeulp, typedata=self.typedata, url=self.ulp, port=self.port, login=self.login, password=self.password)