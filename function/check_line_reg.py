#Не встроенные в python библиотеки
import regex as re #pip install regex

#Регулярное выражение которое проверяет является ли строка форматом http(s)://example(/):data:data
line_valid = re.compile(r'(https?://[^:]+):(.+)')

#Функция принимающая строку и возвращающая значение True если строка прошла проверку, в противном случае False
def main(line: str) -> bool:
    return True if line_valid.match(line) else False