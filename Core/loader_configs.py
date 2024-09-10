from pathlib import Path
from typing import Generic, TypeVar, Type
from json import load

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class LoaderConfigs(Generic[T]):
    config_model: Type[BaseModel]

    @classmethod
    def init_config(cls, path: Path) -> T:
        '''
        Инициализация конфига из файла
        Если файл существует - Загружаем конфиг из него
        Иначе создаёи стандартный конфиг и возвращаем его
        '''
        if path.is_file():
            with path.open(encoding='utf-8') as config_file:
                config_dict = load(config_file)
                config = cls.config_model().model_validate(config_dict)
                return config

        config_string = cls.config_model().model_dump_json(indent=2)
        with path.open(mode='a+', encoding='utf-8') as config_file:
            config_file.write(config_string)
        return cls.config_model()
    
    @staticmethod
    def load_config_from_file(path: Path, default: list[str]) -> list[str]:
        '''
        Загрузка списка из файла (если он существует)
        Иначе записываем список default в файл и возвращаем его
        '''
        if path.is_file():
            with path.open(encoding='utf-8') as config_file:
                return [line.strip().lower() for line in config_file if line.strip()]
        
        with path.open(mode='w', encoding='utf-8') as config_file:
            config_file.write('\n'.join(default))
        
        return default
