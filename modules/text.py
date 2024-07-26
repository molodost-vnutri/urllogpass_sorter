from urllib.parse import urlparse
from typing import Optional

from regex import compile as recompile

from modules.file import bad_list, config
from modules.submodules import SUlp
from modules.shemas import SText

repl_list = [';', ' ', '|']
bad_repl: list[str] = ["(", ")", "*", "$", "!", "%", "&", "^", "#", "<", ">", "?", ";", "~", "=", "[", "]", "'", '"', '+', '/', '\\', ',']
email_regex = recompile(r"^(?!.*\*).+\@.+\..+$")
login_regex = recompile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
number_regex = recompile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")

class Text(SText):
    typeulp = None
    typedata = None
    def __init__(self, ulp: str):
        self.ulp = ulp
        self.result = self.__get__()
    def __check_all_len__(self):
        if len(self.ulp) > 100:
            self.valid = False
            return
    def __isascii__(self):
        return self.ulp.isascii()
    def __check_bad_words__(self):
        if not self.__isascii__():
            self.valid = False
            return
        ulp = self.ulp.lower()
        if any(bad in ulp for bad in bad_list):
            self.valid = False
            return
        del ulp
    def __get_typeulp__(self):
        if self.ulp.startswith("http"): self.typeulp = 0
        elif self.ulp.startswith("android://"): self.typeulp = 1
        elif self.ulp.count("http") == 1 and self.ulp.count("://") == 1: self.typeulp = 2
        else:
            self.typeulp = 0
            self.ulp = "https://"+self.ulp
    def __check_host__(self, url):
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
    def __get_credit__(self):
        if not self.valid:
            return
        for char in repl_list:
            self.ulp = self.ulp.replace(char, ':')
        
        if not self.ulp.count(":") in range(2, 5):
            self.valid = False
            return
        
        self.__get_typeulp__()
        
        parts = self.ulp.split(':')

        if self.typeulp == 2:
            self.login = parts.pop(0)
            self.password = parts.pop(0)
            url = ':'.join(parts)
            self.__check_host__(url)
            return
        
        self.password = parts.pop(-1)
        self.login = parts.pop(-1)
        url = ':'.join(parts)

        if self.typeulp != 1:
            self.__check_host__(url)
            if not self.valid:
                return
    def __find_type__(self):
        if not self.valid:
            return
        for char in bad_repl:
            self.login = self.login.replace(char, "")
        
        if len(self.password) not in range(config.password_len[0], config.password_len[1]):
            self.valid = False
            return
        if config.parse_email:
            if email_regex.match(self.login):
                if len(self.login.split("@")[0]) in range(config.email_len[0], config.email_len[1]):
                    self.typedata = 0
                    return
        if config.parse_login:
            if login_regex.match(self.login) and len(self.login) in range(config.login_len[0], config.login_len[1]):
                self.typedata = 1
                return
        if config.parse_number:
            if number_regex.match(self.login) and len(self.login) in range(config.number_len[0], config.number_len[1]):
                self.typedata = 2
                return
        self.valid = False
    def __get__(self) -> Optional[SUlp]:
        self.__check_all_len__()
        self.__check_bad_words__()
        self.__get_credit__()
        self.__find_type__()
        if self.valid:
            if self.typeulp != 1:
                self.typeulp = 0
            return SUlp(
                typeulp=self.typeulp,
                typedata=self.typedata,
                url=self.url,
                port=self.port,
                login=self.login,
                password=self.password
                )
