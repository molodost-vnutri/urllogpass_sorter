from typing import Optional

Slogin_type = {
    0: "email",
    1: "login",
    2: "number"
}

Sulp_type = {
    0: "http",
    1: "android"
}


class SUlp:
    def __init__(self,
                 typeulp: int,
                 typedata: int,
                 url: str,
                 port: Optional[int],
                 login: str,
                 password: str):
        self.typeulp: str = Sulp_type.get(typeulp)
        self.typedata: str = Slogin_type.get(typedata)
        self.url: str = url
        self.port: Optional[int] = port
        self.login: str = login
        self.password: str = password
        self.full = self.__extract_full_line__()
        self.credit = self.__extract_credit__()
    
    def __extract_credit__(self) -> str:
        return f"{self.login}:{self.password}"
    def __extract_full_line__(self) -> str:
        return f"{self.url}{':' + str(self.port) if self.port else ''}:{self.login}:{self.password}"

