from os import name, system

from colorama import Fore, init

init()

class Logo:
    version = "1.2"
    telegram = "@M0l0d0st_vnutri"
    forum = "https://zelenka.guru/members/3060240"
    thread = "https://zelenka.guru/threads/5830632"
    github = "https://github.com/molodost-vnutri/urllogpass_sorter"

    def __init__(self):
        self.logo = self.logo_cls()
    def logo_cls(self):
        system('cls') if name == 'nt' else system('clear')

        return f'''{Fore.GREEN}

██╗░░░░░░█████╗░██╗░░░░░███████╗████████╗███████╗░█████╗░███╗░░░███╗
██║░░░░░██╔══██╗██║░░░░░╚════██║╚══██╔══╝██╔════╝██╔══██╗████╗░████║
██║░░░░░██║░░██║██║░░░░░░░███╔═╝░░░██║░░░█████╗░░███████║██╔████╔██║
██║░░░░░██║░░██║██║░░░░░██╔══╝░░░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║
███████╗╚█████╔╝███████╗███████╗░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
╚══════╝░╚════╝░╚══════╝╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝{Fore.RESET}
         Сделал molodost vnutri для форума zelenka.guru
         Контакты и ссылки для фидбека:
             [{Fore.LIGHTBLUE_EX}Telegram{Fore.RESET}]=> {self.telegram}
             [{Fore.GREEN}Форум{Fore.RESET}]=> {self.forum}
             [{Fore.GREEN}Тема на форуме{Fore.RESET}]=> {self.thread}
             [{Fore.LIGHTBLACK_EX}Github{Fore.RESET}]=> {self.github}
         Версия: {Fore.GREEN}{self.version}{Fore.RESET}\n\n'''
logo = Logo().logo