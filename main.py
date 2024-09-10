from Core.select_path import get_current_path

from Core.main import run
from Core.schemes import SResultPrint
from Core.logo import logo


if __name__ == '__main__':
    path = get_current_path()
    logo()
    result = run(path)
    SResultPrint(result).print_result()