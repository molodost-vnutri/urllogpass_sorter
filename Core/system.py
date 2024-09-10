from os import name, system
from datetime import datetime

from colorama import init

init(autoreset=True)

current_date = datetime.now().strftime('%Y-%m-%d')

def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')