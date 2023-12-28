#Встроенные в python библиотеки
from os import system, name

#Функция которая очищает экран windows/linux/mac os
def main() -> None:
    system('cls') if name == 'nt' else system('clear')