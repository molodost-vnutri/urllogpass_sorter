def regex_check(data: str, password: str, config: {}) -> str or None:
    import regex

    data, password = data.replace(' ', ''), password.replace(' ', '')
    bad_word = ['http', 'unknown', 'null']

    email_regex = regex.compile(r"^\S+@\S+\.\S+$")
    login_regex = regex.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
    number_regex = regex.compile(r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$")
    password_regex = regex.compile(r"^[ -~]+$")

    if password_regex.match(password):
        if config['email_parse']:
            if email_regex.match(data): return 'email'
        if config['login_parse']:
            if login_regex.match(data) and all(bad not in data.lower() for bad in bad_word): return 'login'
        if config['number_parse']:
            if number_regex.match(data): return 'number'