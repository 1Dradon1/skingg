class CONFIG:
    steam_parsing_delay = 0.8  # дилей в секундах, чтобы парсить скины из стима, меньше 0.8 будут ошибки | стандарт 0.8
    sort_by = "popularity_desc"  # режим сортировки стандартно popularity_desc
    hold = "8"  # скины с холдом в сколько дней хотим парсить, если хотим парсить все оставляем поле пустым
    login = ""  # логин в стиме
    password = ""  # пароль в стиме
    shared_secret = ""  # находится в мафайле вроде самый первый
    SecretAPIKey = ""  # секретный ключ апи от апи стима
    black_list_path = ""  # полный путь до blacklist'а
    white_list_path = "white_list.txt"  # полный путь до whitelist'а
    skingg_page = 1  # с какой странички начнем | стандартно 1
    steam_price_multiply = 0.6  # skingg_price > steam_price * steam_price_multiply | стандартно 0.62
    brute_force_mode = 0  # 0-без фильтра  1-blacklist  2-whitelist | стандартно 0
    min_price = 0  # минимальная цена для покупки в долларах | стандартно 0
    max_price = 1000  # максимальная цена для покупки в долларах | стандартно 100
    proxies = [""]  # прокси в формате xxx.xxx.xxx.xxx:xxxxx:login:password
