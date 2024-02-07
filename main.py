import file_utils
import time

path = file_utils.get_path()
start = time.time()
file_utils.working(path)
end = time.time() - start
minut = int(end // 60)
seconds = end % 60
second = round(seconds,2)
input(f'\nСпарсил за: {minut} минут и {second} секунд')