from typing import Optional, Type
from urllib.parse import urlparse

from Core.settings import email_regex, login_regex, number_regex, filter_list
from Core.config import config
from Core.schemes import LineEnum, SResultUlp, DataEnum

class Text(SResultUlp):
    line: str
    url: str
    login: str
    password: str
    port: Optional[int] = None

    datatype: Type[DataEnum] = DataEnum.default
    schema_length_validator: tuple[int, int] = config.default_length
    valid: bool = True


    def checking_bad_words_in_full_line(self):
        if any(bad_word in self.line.lower() for bad_word in filter_list):
            self.valid = False
            return

    def validate_url(self):
        try:
            url = urlparse(self.url)
            if url.hostname:
                self.url = 'https://' + url.hostname
                if url.port:
                    self.port = url.port
            return
        except:
            pass

        self.valid = False

    def find_datetype(self):
        if not self.valid:
            return
        
        if not config.use_regex:
            return

        if config.parse_email:
            if email_regex.fullmatch(self.login):
                self.datatype = DataEnum.email
                self.schema_length_validator = config.email_length
                return
        
        if config.parse_login:
            if login_regex.fullmatch(self.login):
                self.datatype = DataEnum.login
                self.schema_length_validator = config.login_length
                return
        
        if config.parse_number:
            if number_regex.fullmatch(self.login):
                self.datatype = DataEnum.number
                self.schema_length_validator = config.number_length
                return
        
        self.valid = False
    

    def validate_credit_length(self):
        if not self.valid:
            return
        
        if not config.check_length:
            return
        
        password_length = len(self.password)

        if config.password_length[0] > password_length:
            self.valid = False
            return
        
        if config.password_length[1] < password_length:
            self.valid = False
            return
        
        login_length = len(self.login)

        if self.schema_length_validator[0] > login_length:
            self.valid = False
            return
        
        if self.schema_length_validator[1] < login_length:
            self.valid = False
            return
    
    
    def __init__(self, url: str, login: str, password: str):
        self.url = url
        self.login = login
        self.password = password
        self.line = '{}:{}:{}'.format(url, login, password)

    @classmethod
    def get_result(cls, url: str, login: str, password: str, linetype: Type[LineEnum]) -> Optional[SResultUlp]:
        init_module = cls(url, login, password)

        init_module.checking_bad_words_in_full_line()
        init_module.find_datetype()
        init_module.validate_credit_length()

        if init_module.valid:
            return SResultUlp(
                url=init_module.url,
                port=init_module.port,
                login=init_module.login,
                password=init_module.password,
                datatype=init_module.datatype,
                linetype=linetype
            )