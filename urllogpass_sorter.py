#Импорт библиотек
import os
import io
import sys
import json
import time
try:
	import regex as re
except:
	os.system("pip install regex")
	import regex as re
from glob import glob as gl

#Получение настроек из файла конфигурации
with open("config.json", 'r') as config_file:
    config = json.load(config_file)
zapros = config["zapros"]
sort = config["sort"]
parse_full = config["parse_full"]
bad_char = config["bad_char"]
parse_zapros = config["parse_zapros"]
folder = config["folder"]
size = config["size"]
file_block = config["file_block"]
email_parse = config["email_parse"]
login_parse = config["login_parse"]
number_parse = config["number_parse"]
#Проверка существования папки и назначение пути сохранения
os.mkdir(folder) if not os.path.exists(folder) else None
Result_folder = os.path.join(os.getcwd(), folder)

#Объявляем переменные
Dict = {key: [] for key in zapros}
all_line= 0
size_files = 0

#Регулярные выражения
email_regex = re.compile(r"^\S+@\S+\.\S+$")
login_regex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
number_regex = re.compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")
password_regex = re.compile(r"^[ -~]+$")

#Функция очистки консоли
def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("       Сортировщик url:login:password v0.5\n              сделал molodost_vnutri\n             для форума zelenka.guru\n      https://zelenka.guru/molodost_vnutri\n")

#Функция проверки строки на валидность
def is_valid_line(line):
    parts = line.strip().split(":")
    return len(parts) == 2

#Функция записи данных в файлы
def write():
    global Dict
    for key, values in Dict.items():
        if values:  # Проверка, есть ли значения в словаре
            with open(f"{folder}/{key}.txt", "a", errors='ignore') as file:
                for value in values:
                    file.write(value + "\n")
    Dict.clear()

#Проверка заполненности словаря
def check_size(size):
    global Dict
    dict_count = sum(len(values) for values in Dict.values())
    if dict_count >= size:
        write()
        Dict = {key: [] for key in zapros}

#Функция сортировки строк
def sorting(data, password, line, size):
    global email, login, number, Dict
    if 5 <= len(password) <= 25 and password_regex.match(password) and 5 <= len(data):
        if parse_zapros == True:
            for key in zapros:
                if key in line:
                    if email_parse == True:
                        if email_regex.match(data) and len(data) >= 9:
                            email += 1
                            if sort == 1:
                                Dict.setdefault(f"{key}_email", []).append(f"{data}:{password}")
                                if parse_full == True:
                                    Dict.setdefault(f"{key}_email_full_line", []).append(line)
                            elif sort == 2:
                                Dict.setdefault(key, []).append(f"{data}:{password}")
                                if parse_full == True:
                                    Dict.setdefault(f"{key}_full_line", []).append(line)
                    if login_parse == True:
                        if login_regex.match(data) and all(bad not in data for bad in bad_char):
                            login += 1
                            if sort == 1:
                                Dict.setdefault(f"{key}_login", []).append(f"{data}:{password}")
                                if parse_full == True:
                                    Dict.setdefault(f"{key}_login_full_line", []).append(line)
                            elif sort == 2:
                                Dict.setdefault(key, []).append(f"{data}:{password}")
                                if parse_full == True:
                                    Dict.setdefault(f"{key}_full_line", []).append(line)
                    if number_parse == True:
                        if number_regex.match(data) and all(bad not in data for bad in bad_char) and 6 <= len(data) <= 15:
                            number += 1
                            if sort == 1:
                                Dict.setdefault(f"{key}_number", []).append(f"{data}:{password}")
                                if parse_full == True:
                                    Dict.setdefault(f"{key}_number_full_line", []).append(line)
                            elif sort == 2:
                                Dict.setdefault(key, []).append(f"{data}:{password}")
                                if parse_full == True:
                                    Dict.setdefault(f"{key}_full_line", []).append(line)
        if parse_zapros == False:
            if email_parse == True:
                if email_regex.match(data) and len(data) >= 9:
                    email += 1
                    if sort == 1:
                        Dict.setdefault("data_email", []).append(f"{data}:{password}")
                        if parse_full == True:
                            Dict.setdefault("data_email_full_line", []).append(line)
                    elif sort == 2:
                        Dict.setdefault("data", []).append(f"{data}:{password}")
                        if parse_full == True:
                            Dict.setdefault("data_full_line", []).append(line)
            if login_parse == True:
                if login_regex.match(data) and all(bad not in data for bad in bad_char):
                    login += 1
                    if sort == 1:
                        Dict.setdefault("data_login", []).append(f"{data}:{password}")
                        if parse_full == True:
                            Dict.setdefault("data_login_full_line", []).append(line)
                    elif sort == 2:
                        Dict.setdefault("data", []).append(f"{data}:{password}")
                        if parse_full == True:
                            Dict.setdefault("data_full_line", []).append(line)
            if number_parse == True:
                if number_regex.match(data) and all(bad not in data for bad in bad_char) and 6 <= len(data) <= 15:
                    number += 1
                    if sort == 1:
                        Dict.setdefault("data_number", []).append(f"{data}:{password}")
                        if parse_full == True:
                            Dict.setdefault("data_number_full_line", []).append(line)
                    elif sort == 2:
                        Dict.setdefault("data", []).append(f"{data}:{password}")
                        if parse_full == True:
                            Dict.setdefault("data_full_line", []).append(line)
        check_size(size)
#Функция чтения блока данных полученных от функции read_file
def process_chunk(chunk):
    global all_line
    lines = chunk.split('\n')
    for line in lines:
        all_line += 1
        line = line.replace(" ", ":")
        filtered_line = ":".join(line.strip().split(":")[-2:])
        if is_valid_line(filtered_line):
            data, password = filtered_line.split(":")
            sorting(data, password, line, size)

#Функция читающая файл и отправляющая чанки в функцию process_chunk
def read_file(txt, block_size=file_block * 1024 * 1024):
    with open(txt, 'rb') as file:
        while True:
            block = file.read(block_size)
            if not block:
                break
            with io.BytesIO(block) as buffer:
                while True:
                    chunk = buffer.read(1024*4)
                    if not chunk:
                        break
                    process_chunk(chunk.decode('utf-8', errors='ignore'))
    write()

#Получение пути с файлами от пользователя
while True:
    clear()
    base = input(r"""Работает drag and drop
[Папка с txt]=> """)
    base = base.replace('"', '') if '"' in base else base.replace("'", "")
    if os.path.exists(base):
        break
    input("Папка не найдена")

#Начало работы скрипта
clear()
print("Настройка текущей сессии:")
print(f"Папка с файлами: {base}")
print(f"Парсим: {'Всё' if parse_zapros == False else 'Запросы'}")
print(f"Тип сортировки: {'Три файла' if sort == 1 else 'Всё в один файл'}")
print(f"Какие пары парсим: {'email:pass' if email_parse == True else ''} {'login:pass' if login_parse == True else ''} {'number:pass' if number_parse == True else ''}")
print(f"Парс полных строк: {'Да' if parse_full == True else 'Нет'}")
print(f"{'Запрос: '+' | '.join(zapros) if parse_zapros == True else ''}")
for txt in gl(f"{base}/*.txt"):
    email = 0
    login = 0
    number = 0
    start = time.time()
    size_file_bytes = os.stat(txt).st_size
    size_file_mb = size_file_bytes / (1024 * 1024)
    size_files += size_file_mb
    read_file(txt)
    mail_count = f" | mail:pass: {email}"
    login_count = f" |login:pass: {login}"
    number_count = f" | number:pass: {number}"
    if (email_parse and not login_parse and not number_parse) or (email_parse and not login_parse and not number_parse) or (email_parse and not login_parse and not number_parse):
        all_result = ''
    else:
        all_result = f" | all found: {email+login+number}"
    print(f"{txt}{mail_count if email_parse == True else ''}{login_count if login_parse == True else ''}{number_count if number_parse == True else ''}{all_result} | count line: {all_line} | size file: {round(size_file_mb)}mb")
    write()
end = time.time() - start
minut = int(end // 60)
seconds = end % 60
second = round(seconds,2)
input(f"Скрипт закончил работу за {minut} минут и {second} секунд\nОбработано {round(size_files)}мб")
