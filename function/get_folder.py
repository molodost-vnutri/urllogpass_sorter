# Встроенные в python библиотеки
from os import path

# Модули из папки function
from function import clear

# Функция получающая путь от пользователя
# Если путь корректен, то возвращает путь
def main() -> str:
    while True:
        clear.main()
        base = input('Работает drag&drop\nПеретащите ваш(у) папку или файл в консоль\n[data]=> ').replace('"', '').replace("& '", '').replace("'", '')
        if path.exists(base):
            return base
        input(f'path {base} not exists')
