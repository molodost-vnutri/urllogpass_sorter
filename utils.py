def logo() -> None:
    import colorama
    import os

    colorama.init()
    COLOR = colorama.Fore

    os.system('cls') if os.name == 'nt' else os.system('clear')

    print(f'''{COLOR.GREEN}

██╗░░░░░░█████╗░██╗░░░░░███████╗████████╗███████╗░█████╗░███╗░░░███╗
██║░░░░░██╔══██╗██║░░░░░╚════██║╚══██╔══╝██╔════╝██╔══██╗████╗░████║
██║░░░░░██║░░██║██║░░░░░░░███╔═╝░░░██║░░░█████╗░░███████║██╔████╔██║
██║░░░░░██║░░██║██║░░░░░██╔══╝░░░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║
███████╗╚█████╔╝███████╗███████╗░░░██║░░░███████╗██║░░██║██║░╚═╝░██║
╚══════╝░╚════╝░╚══════╝╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝{COLOR.RESET}
         Сделал molodost vnutri для форума zelenka.guru
         Контакты и ссылки для фидбека:
             [{COLOR.LIGHTBLUE_EX}Telegram{COLOR.RESET}]=> @M0l0d0st_vnutri
             [{COLOR.GREEN}Форум{COLOR.RESET}]=> https://zelenka.guru/members/3060240
             [{COLOR.GREEN}Тема на форуме{COLOR.RESET}]=> https://zelenka.guru/threads/5830632
             [{COLOR.LIGHTBLACK_EX}Github{COLOR.RESET}]=> https://github.com/molodost-vnutri/urllogpass_sorter
         Версия: {COLOR.GREEN}0.8{COLOR.RESET}\n\n''')