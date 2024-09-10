from pathlib import Path

from regex import compile

from Core.loader_configs import LoaderConfigs

# Дополнительные настройки для urllogpass модуля
# ------------------------------------------------------------------------------

'''
Регулярные выражения
'''
email_regex = compile(r"^(?!.*\*).+\@.+\..+$")
login_regex = compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
number_regex = compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")

# ------------------------------------------------------------------------------

'''
replace list -> Символы делители (заменяются в строке на :)
Пример
siteexample.com;login|password -> siteexample.com:login:password
'''
replace_list = [';', ' ', '|']


# Обобщённые настройки
# ------------------------------------------------------------------------------

'''
bad replace -> Список запрещённых символов в логине, в случае появлении удаляются
'''
bad_replace: list[str] = ["(", ")", "*", "$", "!", "%", "&", "^", "#", "<", ">", "?", ";", "~", "=", "[", "]", "'", '"', '+', '/', '\\', ',']

# ------------------------------------------------------------------------------
'''
zapros default -> Используется в том случае если файл zapros.txt не существует
'''
zapros_default: list[str] = ['zapros_one', 'zapros_two']

# ------------------------------------------------------------------------------
'''
filter default -> Используется в том случае если файл filter.txt не существует
'''
filter_default: list[str] = ['unknown', 'none', 'null', '[not_saved]']

def init_threads_count() -> int:
    from os import cpu_count
    
    from Core.config import config

    if config.autothreads:
        return cpu_count() - 1
    return config.threads


# Пути настроек и папок модулей
# ------------------------------------------------------------------------------
config_paths: Path = Path('Settings')


# ------------------------------------------------------------------------------

urllogpass_path: Path = Path('urllogpass')

urllogpass_config: Path = config_paths.joinpath('config.json')
try:
    if not config_paths.is_dir():
        config_paths.mkdir()

    if not urllogpass_path.is_dir():
        urllogpass_path.mkdir(parents=True)
except:
    pass
# ------------------------------------------------------------------------------

filter_path: Path = config_paths.joinpath('filter.txt')
zapros_path: Path = config_paths.joinpath('zapros.txt')

zapros_list = LoaderConfigs.load_config_from_file(zapros_path, zapros_default)
filter_list = LoaderConfigs.load_config_from_file(filter_path, filter_default)

# ------------------------------------------------------------------------------