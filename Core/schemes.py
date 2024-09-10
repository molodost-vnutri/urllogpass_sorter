from typing import Type

from colorama import Fore

class DataEnum:
    login = 'login'
    email = 'email'
    number = 'number'
    default = 'default'

class LineEnum:
    http = 'http'
    android = 'android'
    reversed_http = 'reversed_http'

class SResultUlp:
    url: str
    port: int
    login: str
    password: str
    datatype: Type[DataEnum]
    linetype: Type[LineEnum]

    def __init__(self, url: str, port: int, login: str, password: str, datatype: Type[DataEnum], linetype: Type[LineEnum]):
        self.url = url
        self.port = port
        self.login = login
        self.password = password
        self.datatype = datatype
        self.linetype = linetype

    @property
    def credits(self) -> str:
        return f'{self.login}:{self.password}'

    @property
    def urllogpass(self) -> str:
        if not self.port:
            return f'{self.url}:{self.login}:{self.password}'
        return f'{self.url}:{self.port}:{self.login}:{self.password}'

class SResultSpawner:
    finding_lines: int = 0
    result: dict[str, set[str]] = {}
    result_count: dict[str, int] = {}

    def __init__(self, results: list[dict[str, set[str]]]):    
        for result in results:
            for key, value in result.items():
                if not str(key).endswith('full'):
                    self.finding_lines += len(value)
                    if key not in self.result_count:
                        self.result_count[key] = 0
                    self.result_count[key] += len(value)
                if key not in self.result:
                    self.result[key] = set()
                self.result[key].update(value)

class SResultMain:
    results: dict[str, set[str]] = {}
    any_results_full: dict[str, int] = {}
    any_find_lines: int = 0
    def __init__(self):
        pass

    def append_result(self, result: SResultSpawner):
        for key, value in result.result.items():
            if key not in self.results:
                self.results[key] = set()
            self.results[key].update(value)
        for key, value in result.result_count.items():
            if key not in self.any_results_full:
                self.any_results_full[key] = 0
            self.any_results_full[key] += value
        self.any_find_lines += result.finding_lines


class SResultPrint:
    def __init__(self, result: SResultMain):
        self.result = result
    
    def print_result(self):
        max_key_len = max(len(key) for key in self.result.any_results_full)
        for key, value in self.result.any_results_full.items():
            print(f"{Fore.CYAN}{key.ljust(max_key_len)}: {Fore.GREEN}{str(value).ljust(max_key_len)}")
        print(Fore.RESET + f'\nВсего найдено: {self.result.any_find_lines}')