import os, io
import regex as re
from glob import glob as gl
import time 
os.mkdir("Result") if not os.path.exists("Result") else None
Result_folder = os.path.join(os.getcwd(), "Result")
trash_Dict, trash_zapros_Dict, login_Dict, email_Dict, number_Dict, full_line_Dict = [], [], [], [], [], []
bad_char = ["UNKNOWN", "http", "ftp", "FTP", "unknown", "https", "@"]
email_regex = re.compile(r"^\S+@\S+\.\S+$")
login_regex = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
number_regex = re.compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")
password_regex = re.compile(r"^[ -~]+$")
zapros = None
file_block = 256
size_files = 0
all_line = 0
def clear():
    os.system("cls") if os.name == "nt" else os.system("clear")
    print("       Сортировщик url:login:password v0.4\n              сделал molodost_vnutri\n             для форума zelenka.guru\n      https://zelenka.guru/molodost_vnutri\n")
def is_valid_line(line):
    parts = line.strip().split(":")
    return len(parts) == 2
def del_dup():
    global email_Dict, login_Dict, number_Dict, full_line_Dict, trash_Dict, trash_zapros_Dict
    email_set = set(email_Dict)
    trash_zapros_set = set(trash_zapros_Dict)
    login_set = set(login_Dict)
    number_set = set(number_Dict)
    full_line_set = set(full_line_Dict)
    trash_set = set(trash_Dict)
    email_Dict = list(email_set)
    login_Dict = list(login_set)
    number_Dict = list(number_set)
    full_line_Dict = list(full_line_set)
    trash_Dict = list(trash_set)
    trash_zapros_Dict = list(trash_zapros_Dict)
def write_dict_to_result(zapros, parse_full, sort):
    if zapros == None:
        if sort == 1:
            result_email = os.path.join(Result_folder, "Email_result.txt")
            result_login = os.path.join(Result_folder, "Login_result.txt")
            result_trash = os.path.join(Result_folder, "Trash_result.txt")
            result_number = os.path.join(Result_folder, "Number_result.txt")
            result_line = os.path.join(Result_folder, "Line_result.txt")
            with open(result_email, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as email:
                email.write('\n'.join(email_Dict))
            with open(result_login, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as login:
                login.write('\n'.join(login_Dict))
            with open(result_number, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as number:
                number.write('\n'.join(number_Dict))
            if parse_full == 1:
                with open(result_line, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as all_line:
                    all_line.write('\n'.join(full_line_Dict))
            if write_trash == 1:
                with open(result_trash, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as trash:
                    trash.write('\n'.join(trash_Dict))
        if sort == 2:
            result = os.path.join(Result_folder, "Result.txt")
            result_line = os.path.join(Result_folder, "Line_result.txt")
            result_trash = os.path.join(Result_folder, "Trash_result.txt")
            with open(result, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as result:
                result.write('\n'.join(email_Dict))
                result.write('\n'.join(login_Dict))
                result.write('\n'.join(number_Dict))
            if parse_full == 1:
                with open(result_line, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as all_line:
                    all_line.write('\n'.join(full_line_Dict))
            if write_trash == 1:
                with open(result_trash, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as trash:
                    trash.write('\n'.join(trash_Dict))
    else:
        zapros = zapros.replace("/", "")
        zapros = zapros.replace("\\", "")
        if sort == 1:
            result_email = os.path.join(Result_folder, f"Email_{zapros}.txt")
            result_login = os.path.join(Result_folder, f"Login_{zapros}.txt")
            result_trash = os.path.join(Result_folder, f"Trash_{zapros}.txt")
            result_number = os.path.join(Result_folder, f"Number_{zapros}.txt")
            result_line = os.path.join(Result_folder, f"Line_{zapros}.txt")
            with open(result_email, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as email:
                email.write('\n'.join(email_Dict))
            with open(result_login, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as login:
                login.write('\n'.join(login_Dict))
            with open(result_number, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as number:
                number.write('\n'.join(number_Dict))
            if parse_full == 1:
                with open(result_line, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as all_line:
                    all_line.write('\n'.join(full_line_Dict))
            if write_trash == 1:
                with open(result_trash, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as trash:
                    trash.write('\n'.join(trash_zapros_Dict))
        if sort == 2:
            result = os.path.join(Result_folder, f"{zapros}.txt")
            result_line = os.path.join(Result_folder, f"Line_{zapros}.txt")
            result_trash = os.path.join(Result_folder, f"Trash_{zapros}.txt")
            with open(result, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as result:
                result.write('\n'.join(email_Dict))
                result.write('\n'.join(login_Dict))
                result.write('\n'.join(number_Dict))
            if parse_full == 1:
                with open(result_line, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as all_line:
                    all_line.write('\n'.join(full_line_Dict))
            if write_trash == 1:
                with open(result_trash, "a+", encoding="utf-8", errors="ignore", buffering=1024 * 1024 * 16) as trash:
                    trash.write('\n'.join(trash_zapros_Dict))
def process_large_file(txt, block_size=file_block * 1024 * 1024):
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
                    process_chunk(chunk.decode('utf-8', errors='ignore'), zapros, parse_full)
def sorting(data, password, parse_full, line, zapros):
    global count_email, count_login, count_number
    data = data.replace(":", '')
    data = data.replace("(", '')
    data = data.replace(")", '')
    data = data.replace("+", '')
    if 5 <= len(password) <= 25 and password_regex.match(password) and 5 <= len(data):
        if email_regex.match(data) and len(data) >= 9:
            email_Dict.append(f"{data}:{password}")
            if parse_full == 1:
                full_line_Dict.append(line)
        elif login_regex.match(data) and all(bad not in data for bad in bad_char):
            login_Dict.append(f"{data}:{password}")
            if parse_full == 1:
                full_line_Dict.append(line)
        elif number_regex.match(data) and all(bad not in data for bad in bad_char) and 6 <= len(data) <=15:
            number_Dict.append(f"{data}:{password}")
            if parse_full == 1:
                full_line_Dict.append(line)
        else:
            if write_trash == 1:
                if zapros is not None and zapros in line:
                    trash_zapros_Dict.append(line)
                else:
                    trash_Dict.append(line)
    else:
        if write_trash == 1:
            if zapros is not None and zapros in line:
                trash_zapros_Dict.append(line)
            else:
                trash_Dict.append(line)
def process_chunk(chunk, zapros, parse_full):
    global all_line, count_trash
    lines = chunk.split('\n')
    for line in lines:
        line = line.replace(" ", ":")
        if zapros == None:
            all_line +=1
            filtered_line = ":".join(line.strip().split(":")[-2:])
            if is_valid_line(filtered_line):
                data, password = filtered_line.split(":")
                sorting(data, password, parse_full, line, zapros)
            else:

                trash_Dict.append(line)
        else:
            all_line +=1
            if zapros in line:
                filtered_line = ":".join(line.strip().split(":")[-2:])
                if is_valid_line(filtered_line):
                    data, password = filtered_line.split(":")
                    sorting(data, password, parse_full, line, zapros)
                else:    
                    count_trash +=1    
                    trash_zapros_Dict.append(line)    
while True:
    clear()
    base = input(r"""Работает drag and drop
[Папка с txt]=> """)
    base = base.replace('"', '') if '"' in base else base.replace("'", "")
    if os.path.exists(base):
        break
    input("Папка не найдена")
while True:
    clear()
    select = input("1) Парсить всё\n2) Парсить запрос\n[Выбор]=> ")
    try:
        select = int(select)
        if select in [1, 2]:
            break
    except:
        None
while True:
    clear()
    sort = input("Как будем сортировать?\n1) Три файла: mail:pass, login:pass, number:pass\n2) Всё в одном файле\n[Выбор]=> ")
    try:
        sort = int(sort)
        if sort in [1, 2]:
            break
    except:
        None
while True:
    clear()
    parse_full = input("Парсить дополнительно полность строку? (нужно допустим при поиске сайтов с определённым портом или названием которое может быть разное)\nСнижает скорость обработки!\n1) Да\n2) Нет\n[выбор]=> ")
    try:
        parse_full = int(parse_full)
        if parse_full in [1, 2]:
            break
    except:
        None
while True:
    clear()
    write_trash = input("Записывать плохие строки в файл?\nСнижает скорость обработки!\n1) Да\n2) Нет\n[Выбор]=> ")
    try:
        write_trash = int(write_trash)
        if write_trash in [1, 2]:
            break
    except:
        None
while True:
    clear()
    block_select = input("Использовать кастомное значение блоков?\nПо умолчанию: 256mb\n1) Да\n2) Нет\n[Выбор]=> ")
    try:
        block_select = int(block_select)
        if block_select in [1, 2]:
            break
        else:
            None
    except:
        None
if block_select == 1:
    clear()
    while True:
        file_block = input("Введите колличество мб в одном блоке\n[Число мб]=> ")
        try:
            file_block = int(file_block)
            break
        except:
            None
if select == 1:
    start = time.time()
    clear()
    print(f"Настройка текущей сессии:\nПапка с файлами: {base}\nПарсим: всё\nТип сортировки: {'Три файла' if sort == 1 else 'Всё в один файл'}\nПарс строк: {'Да' if parse_full == 1 else 'Нет'}\nЗапись плохих строк: {'Да' if write_trash == 1 else 'Нет'}\nКолличество мб в блоке: {file_block}")
    for txt in gl(f"{base}/*.txt"):
        size_file_bytes = os.stat(txt).st_size
        size_file_mb = size_file_bytes / (1024 * 1024)
        size_files += size_file_mb
        process_large_file(txt)
        del_dup()
        count_email, count_login, count_number, count_trash, count_trash_zapros = len(email_Dict), len(login_Dict), len(number_Dict), len(trash_Dict), len(trash_zapros_Dict)
        print(f"{txt} | mail:pass: {count_email} | login:pass: {count_login} | number:pass: {count_number} | all found: {count_email+count_login+count_number} | count line: {all_line} | size file: {round(size_file_mb)}mb")
        write_dict_to_result(zapros, parse_full, sort)
        trash_Dict, trash_zapros_Dict, login_Dict, email_Dict, number_Dict, full_line_Dict = [], [], [], [], [], []
if select == 2:
    start = time.time()
    clear()
    zapros = input("В формате domain.com\n[Запрос]=> ")
    clear()
    print(f"Настройка текущей сессии:\nПапка с файлами: {base}\nПарсим: всё\nТип сортировки: {'Три файла' if sort == 1 else 'Всё в один файл'}\nПарс строк: {'Да' if parse_full == 1 else 'Нет'}\nЗапись плохих строк: {'Да' if write_trash == 1 else 'Нет'}\nЗапрос: {zapros}\nКолличество мб в блоке: {file_block}")
    for txt in gl(f"{base}/*.txt"):
        size_file_bytes = os.stat(txt).st_size
        size_file_mb = size_file_bytes / (1024 * 1024)
        size_files += size_file_mb
        process_large_file(txt)
        del_dup()
        count_email, count_login, count_number, count_trash, count_trash_zapros = len(email_Dict), len(login_Dict), len(number_Dict), len(trash_Dict), len(trash_zapros_Dict)
        print(f"{txt} | mail:pass: {count_email} | login:pass: {count_login} | number:pass: {count_number} | all found: {count_email+count_login+count_number} | count line: {all_line} | size file: {round(size_file_mb)}mb")
        write_dict_to_result(zapros, parse_full, sort)
        trash_Dict, trash_zapros_Dict, login_Dict, email_Dict, number_Dict, full_line_Dict = [], [], [], [], [], []
end = time.time() - start
minut = int(end // 60)
seconds = end % 60
second = round(seconds,2)
input(f"Скрипт закончил работу за {minut} минут и {second} секунд\nОбработано {round(size_files)}мб")
