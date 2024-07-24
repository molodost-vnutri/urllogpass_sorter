from typing import Optional

from pydantic import BaseModel

class SConfig(BaseModel):
    parse_zapros: bool
    parse_email: bool
    parse_login: bool
    parse_number: bool
    parse_full: bool
    thread_auto: bool
    threads: int
    email_len: tuple[int, int]
    login_len: tuple[int, int]
    number_len: tuple[int, int]
    password_len: tuple[int, int]
    folder: str

class SText:
    url: str
    port: Optional[int] = None
    login: str
    password: str
    typedata: int
    typeulp: int
    valid: bool = True
    bad_list: list[str]
    repl_list: list[str]