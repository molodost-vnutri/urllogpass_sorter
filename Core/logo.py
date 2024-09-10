from colorama import Fore

from Core.system import clear_screen

class Logo:
    version = "1.3 pre-release"
    telegram = "@M0l0d0st_vnutri"
    forum = "https://zelenka.guru/members/3060240"
    thread = "https://zelenka.guru/threads/5830632"
    github = "https://github.com/molodost-vnutri/urllogpass_sorter"

    @classmethod
    def logo_cls(cls):
        clear_screen()

        print(f'''{Fore.GREEN}

██╗░░░░░░█████╗░██╗░░░░░███████╗████████╗███████╗░█████╗░███╗░░░███╗
██║░░░░░██╔══██╗██║░░░░░╚════██║╚══██╔══╝██╔════╝██╔══██╗████╗░████║
██║░░░░░██║░░██║██║░░░░░░░███╔═╝░░░██║░░░█████╗░░███████║██╔████╔██║
██║░░░░░██║░░██║██║░░░░░██╔══╝░░░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║
███████╗╚█████╔╝███████╗███████╗░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
╚══════╝░╚════╝░╚══════╝╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝{Fore.RESET}
         Сделал molodost vnutri для форума zelenka.guru
         Контакты и ссылки для фидбека:
             [{Fore.LIGHTBLUE_EX}Telegram{Fore.RESET}]=> {cls.telegram}
             [{Fore.GREEN}Форум{Fore.RESET}]=> {cls.forum}
             [{Fore.GREEN}Тема на форуме{Fore.RESET}]=> {cls.thread}
             [{Fore.LIGHTBLACK_EX}Github{Fore.RESET}]=> {cls.github}
         Версия: {Fore.GREEN}{cls.version}{Fore.RESET}\n\n''')
logo = Logo().logo_cls