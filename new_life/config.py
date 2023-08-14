class CONFIG:
    steam_parsing_delay = 3  # дилей в секундах, что бы парсить скины из стима, меньше 3 будут ошибки | стандартно 3
    sort_by = "popularity_desc"  # режим сортировки стандартно popularity_desc
    hold = "8"  # скины с холдом в сколько дней хотим парсить, если хотим парсить все оставляем поле пустым
    login = ""  # логин в стиме
    password = "asdasd"  # пароль в стиме
    shared_secret = ""  # находится в мафайле вроде самый первый
    black_list_path = ""  # полный путь до blacklist'а
    white_list_path = ""  # полный путь до whitelist'а
    skingg_page = 1  # с какой странички начнем | стандартно 1
    steam_price_multiply = 0.62  # skingg_price > steam_price * steam_price_multiply | стандартно 0.62
    brute_force_mode = 0  # 0 - без фильтра 1 - blacklist 2 - whitelist | стандартно 0

