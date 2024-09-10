from Core.config import result_folder


def write_results(results: dict[str, set[str]]):
    for key, value in results.items():
        if value:
            with open(result_folder.joinpath(f'{key}.txt'), mode='a+', encoding='utf-8') as file:
                file.write('\n'.join(value))