from typing import Optional

from Core.config import config
from Core.schemes import LineEnum, SResultUlp
from Core.settings import replace_list, bad_replace
from Core.Text_validator import Text

class Unzip(Text):
    line: str
    port: Optional[int] = None
    valid: bool = True

    def validate_full_length(self):
        if not config.check_length:
            return
        
        line_length = len(self.line)
        
        if line_length < config.all_length[0]:
            self.valid = False
            return
        
        if line_length > config.all_length[1]:
            self.valid = False
    
    def get_credit_in_line(self):
        if not self.valid:
            return
        
        for char in replace_list:
            self.line.replace(char, ':')
        
        if not self.line.count(':') in range(2, 5):
            self.valid = False
            return
        
        self.get_typeulp_line()

        parts = self.line.split(':')

        if self.linetype == LineEnum.reversed_http:
            self.login = parts.pop(0)
            self.password = parts.pop(0)
            self.url = ':'.join(parts)
            self.linetype = LineEnum.http
        
        else:
            self.password = parts.pop()
            self.login = parts.pop()
            self.url = ':'.join(parts)
        
        del parts

        for char in bad_replace:
            self.login.replace(char, '')
    
    def get_typeulp_line(self):
        if self.line.startswith('http://') or self.line.startswith('https://'):
            self.linetype = LineEnum.http
        elif self.line.startswith('android://'):
            self.linetype = LineEnum.android
        elif self.line.count('http') and self.line.count('://'):
            self.linetype = LineEnum.reversed_http
        else:
            self.linetype = LineEnum.http
            self.line = 'https://' + self.line
    
    def __init__(self, line: str):
        self.line = line
    
    @classmethod
    def get_result(cls, line: str) -> Optional[SResultUlp]:
        main_module = cls(line)
        main_module.validate_full_length()
        main_module.get_credit_in_line()
        if main_module.valid:
            return Text.get_result(main_module.url, main_module.login, main_module.password, linetype=main_module.linetype)