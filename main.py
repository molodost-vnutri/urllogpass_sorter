# Модули из папки function
from function import get_folder, read_file, check_path, clear # Получаем путь, читаем файл, проверяем папка или файл, очистка экрана

# Встренная библиотека python
from glob import glob

# Не встроенная в python библиотека
from colorama import init, Fore # pip install colorama

init() # Инициализируем цвета
R = Fore.RED # Красный
G = Fore.GREEN # Зелёный
Y = Fore.YELLOW # Жёлтый
RS = Fore.RESET # Сброс цветов

data = get_folder.main()
path = check_path.main(data)


if path[0]:
    clear.main()
    match path[1]:
        case 'file':
            status = read_file.main(data)
            if status[0]:
                print(f'[{G}+{RS}] Закончил файл {data} колличество обработанных строк: {status[1]}')
            else:
                print(f'[{Y}!{RS}] Произошла ошибка в файле {data} ошибка: {status[1]}')
        case 'folder':
            files = glob(f'{data}/*.txt')
            for file in files:
                status = read_file.main(file)
                if status[0]:
                    print(f'Закончил файл {file} колличество обработанных строк: {status[1]}')
                else:
                    print(f'[{Y}!{RS}] Произошла ошибка в файле {file} ошибка: {status[1]}')
            print(f'Всего обработанных файлов: {G}{len(files)}{RS}')
else:
    print(f'[{R}-{RS}] Произошла ошибка при получении файла/папки: {path[0]}')