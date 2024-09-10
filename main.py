from Core.select_path import get_current_path
from Core.loader_paths import loader

from Core.main import run
from Core.schemes import SResultPrint
from Core.logo import logo


if __name__ == '__main__':
    path = get_current_path()
    logo()
    paths = loader.get_files(path)
    result = run(paths)
    SResultPrint(result).print_result()