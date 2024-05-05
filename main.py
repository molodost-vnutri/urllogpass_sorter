from function.user_input import get_path
from function.file import read_paths
import time

start = time.time()

files = get_path()

read_paths(files)
end = time.time() - start
minut = int(end // 60)
seconds = end % 60
second = round(seconds,2)
input(f"Скрипт закончил работу за {minut} минут и {second} секунд")