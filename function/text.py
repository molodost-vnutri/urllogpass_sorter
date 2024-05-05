import regex
from urllib.parse import urlparse

def regexp(data: str, password: str, email: regex, login: regex, number: regex, config: dict) -> int or None: # type: ignore
    if not config["check_regex"]:
        return 3
    if password.isascii():
        if config["email_parse"]:
            if email.match(data):
                return 0
        if config["login_parse"]:
            if login.match(data):
                return 1
        if config["number_parse"]:
            if number.match(data):
                return 2
    return None

def bad_word(data: str, bad_list: list) -> bool:
    data = data.lower()
    return all(bad not in data for bad in bad_list)

def get_credit(line: str, repl_list: list) -> list or None: # type: ignore
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
            url = line.replace(f"{data}:{password}", "").replace("//", "://")
            try:
                if urlparse(f"https://{url}").hostname is not None:
                    return [True, url, data, password]
            except:
                return None
        if "http" in line:
            url = line.replace(f"{parts[0]}:{parts[1]}", "").replace(":", "").replace("//", "://")
            try:
                if urlparse(f"https://{url}").hostname is not None:
                    return [True, url, data, password]
            except:
                return None
        
    return None

def check_len(data: str, password: str, type_data: int, config: dict) -> bool:
    if not config["check_len"]:
        return True
    if config["password_len"][0] < len(password) < config["password_len"][1]:
        if type_data == 0:
            if config["email_len"][0] < len(data) < config["email_len"][1]: return True
        if type_data == 1:
            if config["login_len"][0] < len(data) < config["login_len"][1]: return True
        if type_data == 2:
            if config["number_len"][0] < len(data) < config["number_len"][1]: return True
        if type_data == 3:
            if 5 < len(data) < 30: return True
    return False

def main(line: str, bad_list: list, repl_list: list, email_regex: regex, login_regex: regex, number_regex: regex, config: dict) -> list or None: # type: ignore
    result = get_credit(line=line, repl_list=repl_list)
    if result is None: return None
    url, data, password = result[-3:]
    if not bad_word(data=data, bad_list=bad_list): return None
    result = regexp(data=data, password=password, email=email_regex, login=login_regex, number=number_regex, config=config)
    if result is None: return None
    if not check_len(data=data, password=password, type_data=result, config=config): return None
    return [url, data, password, result]