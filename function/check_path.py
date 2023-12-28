#Встроенные в python библиотеки
from os import path

#Функция получает путь возвращает данные типа [bool, str], если это папка -> [True, 'folder'], файл -> [True, 'file'] в противном случае [False, 'comment']
def main(data: str) -> str:
    if path.isfile(data):
        return [True, 'file']
    if path.isdir(data):
        return [True, 'folder']
    return [False, 'folder not exists']