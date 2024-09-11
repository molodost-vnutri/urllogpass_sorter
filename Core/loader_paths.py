from pathlib import Path
from typing import Union

class Loader:
    path: Path

    @staticmethod
    def validate_path(path: Union[str, Path]) -> Path:
        '''
        Получает путь в виде строки или объекта Path
        Если Получена не строка или объект Path, то программа завершает
        '''

        if isinstance(path, str):
            path = Path(path)
        if not isinstance(path, Path):
            raise TypeError('Путь должен быть строкой или объектом Path')
        return path

    def get_files(self, path: Union[str, Path]) -> list[Path]:
        path = self.validate_path(path)
        '''
        Возвращает список путей с файлами оканчивающимися на .txt
        [Если путь уже является файлом с окончанием .txt, то отдаёт его]
        '''
        if path.is_file():
            return [path]
        
        if path.is_dir():
            paths: list[Path] = []
            for root, _, files in path.walk():
                for file in files:
                    if file.endswith('.txt'):
                        paths.append(root.joinpath(file))
            return paths
        
        raise ValueError('Указанный путь не является директорией или файлом')

    def __init__(self):
        pass

loader = Loader()
