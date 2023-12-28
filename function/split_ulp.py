#Принимает в виде аргумента строку и возвращает последние 2 элемента в том случае если колличество элементов при дроблении на символ : равно 4 ['http', 'domain', 'data', 'password'], в противном случае вернёт пустой массив
def main(line: str) -> []:
    if len(line.split(':')) == 4:
        parts_line = line.split(':')
        return [parts_line[-2], parts_line[-1]]
    return []