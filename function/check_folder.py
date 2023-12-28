#Встроенные в python библиотеки
from json import load
from os import path, mkdir, getcwd


#Парсим значения json файла config.json
with open('config.json') as config_file:
    config = load(config_file)

#Парсим значение folder
folder = config['folder'] #str

#Функция проверяет существование папки в переменной folder если её нет, то создаёт после возвращает путь до неё
def main() -> str:
    mkdir(folder) if not path.isdir(folder) else None
    return path.join(getcwd(), folder)