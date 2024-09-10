from pydantic import field_validator, PositiveInt, BaseModel

from Core.settings import urllogpass_config, zapros_default, zapros_path, filter_default, filter_path, urllogpass_path
from Core.system import current_date
from Core.loader_configs import LoaderConfigs

class ConfigModel(BaseModel):
    '''
    parse_zapros -> Парс запросов из файла zapros.txt, По умолчанию False
    parse_email -> Парс почт, по умолчанию True
    parse_login -> Парсить ли логины из файлов, по умолчанию True
    parse_number -> Парсить ли номера из файлов, по умолчанию True
    parse_full -> Парсить ли полную строку, по умолчанию False
    
    use_regex -> Валидация строк используя регулярные выражения, по умолчанию True
    check_length -> Валидация строк по длине, по умолчанию True

    default_length -> Минимальная и максимальная длина по умолчанию (в случае use_regex = False), по умолчанию (5, 35)
    email_length -> Минимальная и максимальная длина почты, по умолчанию (8, 35)
    login_length -> Минимальная и максимальная длина логина, по умолчанию (5, 35)
    number_length -> Минимальная и максимальная длина номера, по умолчанию (11, 16)
    password_length -> Минимальная и максимальная длина пароля, по умолчанию (8, 35)

    autothreads -> Использовать все ядра кроме последнего, по умолчанию True
    threads -> Количество потоков (в случае autothreads = False), по умолчанию 4
    '''
    parse_zapros: bool = False
    parse_email: bool = True
    parse_login: bool = True
    parse_number: bool = True
    parse_full: bool = False

    use_regex: bool = True
    check_length: bool = True

    default_length: tuple[PositiveInt, PositiveInt] = (5, 35)
    all_length: tuple[PositiveInt, PositiveInt] = (20, 150)

    email_length: tuple[PositiveInt, PositiveInt] = (8, 35)
    login_length: tuple[PositiveInt, PositiveInt] = (5, 35)
    number_length: tuple[PositiveInt, PositiveInt] = (11, 16)
    password_length: tuple[PositiveInt, PositiveInt] = (8, 35)

    autothreads: bool = True
    threads: PositiveInt = 4
    count_line_in_buffer: PositiveInt = 500_000

    folder: str = 'Result'

    @field_validator('default_length', 'email_length', 'login_length', 'number_length', 'password_length')
    def validator_tuple(cls, v: tuple[PositiveInt, PositiveInt]):
        if v[0] > v[1]:
            raise Exception('Минимальная длина должна быть меньше максимальной')
        return v

class Config(LoaderConfigs[ConfigModel]):
    config_model = ConfigModel

config = Config.init_config(urllogpass_config)
zapros_list = LoaderConfigs.load_config_from_file(zapros_path, zapros_default)
filter_list = LoaderConfigs.load_config_from_file(filter_path, filter_default)

result_folder = urllogpass_path.joinpath(config.folder).joinpath(current_date)

if not result_folder.is_dir():
    result_folder.mkdir(parents=True)