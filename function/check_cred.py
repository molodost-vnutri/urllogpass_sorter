#Не встроенные в python библиотеки
from regex import compile #pip install regex

#Встроенные в python библиотеки
from json import load

#Парсим значения json файла config.json
with open('config.json') as config_file:
    config = load(config_file)

#Получаем значения с config.json
email = config['email_parse'] #True/False
login = config['login_parse'] #True/False
number = config['number_parse'] #True/False

#bad word'ы которые не должны находится в data (Исключение email)
bad_char = config['bad_char'] #[]

#Регулярные значения для email/login/number/password
email_regex = compile(r"^\S+@\S+\.\S+$") #mail@example.com
login_regex = compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$") #Любой логин содержащий буквы от aA до zZ и который может содержать цифры и знаки -, _
number_regex = compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$") #Номер который может содержать символы -, (),
password_regex = compile(r"^[ -~]+$") #Пароль содержащий все символы которые можно напечатать

#Функция возвращающая словарь вида [bool, data_type]
#Проверяет что переменная email login или number True, и если два регулярных выражения верны и все bad word не находятся в data (исключение email) возвращает [True, data_type] в противном случае вернёт [False, None]
def main(data: str, password: str) -> [bool, str]:
    if email:
        if email_regex.match(data) and password_regex.match(password):
            return [True, 'email']
    if login:
        if login_regex.match(data) and password_regex.match(password) and all(bad not in data for bad in bad_char):
            return [True, 'login']
    if number:
        if number_regex.match(data) and password_regex.match(password) and all(bad not in data for bad in bad_char) and len(data) >= 7:
            return [True, 'number']
    return [False, None]