from config import CONFIG


def ComparePrices(steam_price: float, skingg_price: float):
    if skingg_price > steam_price * CONFIG.steam_price_multiply:
        return False
    return True


def should_purchase_item(steam_item, skingg_item, brute_force_mode, item_list) -> bool:
    if brute_force_mode == 0:
        if ComparePrices(steam_item.price, skingg_item.price):
            return True

    elif brute_force_mode == 1:
        if skingg_item.name not in item_list:
            if ComparePrices(steam_item.price, skingg_item.price):
                return True

    elif brute_force_mode == 2:
        if skingg_item.name in item_list:
            if ComparePrices(steam_item.price, skingg_item.price):
                return True

    else:
        return False


def get_item_list(brute_force_mode):
    if brute_force_mode == 0:
        return None

    if brute_force_mode == 1:
        items_set = set()

        file_path = CONFIG.black_list_path
        with open(file_path, 'r') as file:
            for line in file:
                item = line.strip()
                items_set.add(item)
        return items_set

    if brute_force_mode == 2:
        items_set = set()

        file_path = CONFIG.white_list_path
        with open(file_path, 'r') as file:
            for line in file:
                item = line.strip()
                items_set.add(item)
        return items_set
