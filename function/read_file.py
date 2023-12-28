#Встроенные в python библиотеки
from json import load

# Модули из папки function
from function import check_cred, check_line_reg, split_ulp, check_folder # Проверка data:password, проверка ulp, получение data:password, получения папки результатов

# Парсим значения json файла config.json
with open('config.json') as config_file:
    config = load(config_file)

file_block = config['file_block'] # int (Сколько строк будет загружено за один блок)
parse_zapros =  config['parse_zapros'] # True/False (Парсинг запроса)
zapros = config['zapros'] #[] (Запросы для парсинга)
parse_line = config['parse_line'] # True/False (Парсинг полной строки)
size = config['size'] # int (Колличество элементов в словаре)

# Получаем путь до папки с результатами
folder = check_folder.main()

# Создаём словарь вида
# {key: [data, data]
#  key: [data, data]}
Dict = {key: [] for key in zapros} 

# Функция для записи данных из словарей в файлы, ничего не возвращает
def write() -> None:
    global Dict
    for key, values in Dict.items():
        if values: # Если в ключе есть какие-то значения, значит создаём файл (для того чтобы не было пустых папок)
            with open(f'{folder}/{key}.txt', 'a', encoding='utf-8', errors='ignore') as file:
                for value in values:
                    file.write(f'{value}\n')
    # Очищаем словарь
    Dict = {key: [] for key in zapros}

# Функция проверяет чтобы колличество элементов не превышало допустимого значения, ничего не возвращает
def check_size() -> None:
    dict_count = sum(len(values) for values in Dict.values())
    if dict_count >= size: # Если словарь достиг максимума, то вызываем функцию write()
        write()

# Функция принимающая путь до файла в виде аргумента и возвращает [bool, msg/int], в случае успешной обработки возвращает [True, count line], в противном случае [False, error msg]
def main(file: str) -> [bool, str or int]:
    lines = 0
    try:
        block_count = 0
        with open(file, encoding='utf-8', errors='ignore') as file_read:
            while True:
                block = file_read.read(file_block * 1024 * 1024)
                if not block:
                    write()
                    return [True, lines]
                block_count += 1
                for line in block.split('\n'):
                    lines += 1
                    line = line.replace(' ', ':', 1).replace(';', ':').replace('::', ':').replace('|', ':').replace(',', ':')
                    sorting(line)
    except Exception as e:
        return [False, e]

# Функция сортировки, принимает в виде аргумента строку, ничего не возвращает
def sorting(line: str) -> None:
    check_size() # Функция проверки колличества элементов в словаре
    if check_line_reg.main(line): # Проверяем подходит ли строка по формату http(s)://u:l:p
        if parse_zapros: # Если работа с запросами
            for key in zapros: #Проходим по запросам
                if key in line: 
                    result_check = split_ulp.main(line) 
                    if result_check[0] != False:
                        result_cred = check_cred.main(result_check[0], result_check[1])
                        if result_cred[0]:
                            Dict.setdefault(f'{key}_{result_cred[1]}', []).append(f'{result_check[0]}:{result_check[1]}')
                            if parse_line:
                                Dict.setdefault(f'{key}_{result_cred[1]}_line', []).append(line)
        else:
            result_check = split_ulp.main(line)
            if result_check:
                result_cred = check_cred.main(result_check[0], result_check[1])
                if result_cred[0]:
                    Dict.setdefault(result_cred[1], []).append(f'{result_check[0]}:{result_check[1]}')
                    if parse_line:
                        Dict.setdefault(f'{result_cred[1]}_line', []).append(line)
