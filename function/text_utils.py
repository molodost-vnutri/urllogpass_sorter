import regex
from urllib.parse import urlparse
def regexp(data: str, password: str, email: regex, login: regex, number: regex, config: dict) -> str:
    if password.isascii():
        if email.match(data) and config["email_parse"]: return "email"
        if login.match(data) and config["login_parse"]: return "login"
        if number.match(data) and config["number_parse"]:return "number"
    return None

def bad_word(data: str, bad_list: list) -> bool:
    data = data.lower()
    return all(bad not in data for bad in bad_list)

def get_credit(line: str, repl_list: list) -> list:
    for repl in repl_list:
        line = line.replace(repl, ":")
    
    if 2 < line.count(":") < 5:
        parts = line.split(":")
        if line.startswith("android"):
            data, password = parts[-2:]
            url = line.replace(f"{data}:{password}", "").replace("//", "://")
            return [True, url, data, password]
        if line.startswith("http"):
            data, password = parts[-2:]
            url = line.replace(f"{data}:{password}", "")
            if urlparse(f"https://{url}").hostname is not None:
                return [True, url, data, password]
        if "http" in line:
            url = line.replace(f"{parts[0]}:{parts[1]}", "").replace(":", "").replace("//", "://")
            if urlparse(f"https://{url}").hostname is not None:
                return [True, url, parts[0], parts[1]]
    return [False, line]

def check_len(data: str, password: str, type_data: str) -> bool:
    if type_data != "number": return 4 < len(data) < 30 and 7 < len(password) < 25
    return 8 < len(data) < 19 and 7 < len(password) < 25


def main(line: str, bad_list: list, repl_list: list, email: regex, login: regex, number: regex, config: dict) -> list:
    result = get_credit(line=line, repl_list=repl_list)
    if not result[0]: return [False, line]
    url, data, password = result[-3:]
    if not bad_word(data=data, bad_list=bad_list): return [False, line]
    result = regexp(data=data, password=password, email=email, login=login, number=number, config=config)
    if result is None: return [False, line]
    if not check_len(data=data, password=password, type_data=result): return [False, line]
    if result is not None: return [True, result, url, data, password]
    return [False, line]