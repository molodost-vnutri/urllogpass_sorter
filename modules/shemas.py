from pydantic import BaseModel, PositiveInt
from typing import Optional

Slogin_type = {
    0: 'email',
    1: 'login',
    2: 'number'
}

Sulp_type = {
    0: 'http',
    1: 'android'
}

class SJson(BaseModel):
    zapros: list[str]
    parse_zapros: bool
    parse_email: bool
    parse_login: bool
    parse_number: bool
    parse_full: bool
    bad_list: list[str]

    thread_auto: bool
    threads: int

    buffer: PositiveInt
    folder: str

class SText:
    url: Optional[str] = None
    port: Optional[PositiveInt] = None
    login: Optional[str] = None
    password: Optional[str] = None
    typedata: Optional[PositiveInt] = None
    typeulp: Optional[PositiveInt] = None
    valid: bool = True

class SFileResult:
    def __init__(self, path):
        self.find: PositiveInt = 0
        self.all_lines: PositiveInt = 0
        self.path: str = path

class SUlp:
    def __init__(self, typeulp: PositiveInt, typedata: int, url: str, port: Optional[int], login: str, password: str):
        self.typeulp: str = Sulp_type.get(typeulp)
        self.typedata: str = Slogin_type.get(typedata)
        self.url: str = url
        self.port: Optional[int] = port
        self.login: str = login
        self.password: str = password
    
    def extract_credit(self) -> str:
        return f'{self.login}:{self.password}'
    def extract_full_line(self) -> str:
        return f'{self.url}{":" + str(self.port) is self.port is not None}:{self.login}:{self.password}'