import time
import traceback
from validate_cheap_item import should_purchase_item, get_item_list
from get_info_form_skingg import *
from item import SkinggItem, SteamItem
from auth import make_auth
from config import CONFIG
import threading
import urllib.parse


def main(brute_force_mode, proxies):
    skingg_page = CONFIG.skingg_page
    item_list = get_item_list(brute_force_mode)
    brute_force_mode = 0
    if brute_force_mode == 2:
        white_list(brute_force_mode, item_list, proxies)
    brute_force(brute_force_mode, item_list, skingg_page, proxies)


def white_list(brute_force_mode, item_list):
    with open("item_buy_log.txt", "a", encoding="utf-8") as file:
        while True:
            try:
                initiativ.acquire()

                for item in item_list:
                    skingg_item, steam_item = get_items_to_compare(item)

                    print(skingg_item.name)

                    purchase_item_if_necessary(brute_force_mode, file, item_list, skingg_item, steam_item)

                print("все шмотки были проверены")

            except Exception as err:
                handle_error(err)
                continue


def brute_force(brute_force_mode, item_list, skingg_page, proxies):
    with open("item_buy_log.txt", "a", encoding="utf-8-sig") as file:
        while True:
            try:
                initiativ.acquire()

                proxy_index = 0
                current_proxy = get_current_proxy(proxies, proxy_index)

                skingg_page_items, skingg_page_count = parse_data_from_skingg_page(skingg_page, CONFIG.sort_by,
                                                                                   CONFIG.hold, current_proxy)
                delay = 24 * skingg_page_count * 18

                for skingg_item_info in skingg_page_items:
                    skingg_item, steam_item = get_items_to_compare(skingg_item_info)

                    print(skingg_item.name)

                    purchase_item_if_necessary(brute_force_mode, file, item_list, skingg_item, steam_item)

                    proxy_index = swap_proxy_if_necessary(skingg_page, proxies, proxy_index)

                skingg_page = await_and_rerun(brute_force_mode, delay, proxies, skingg_page, skingg_page_count)

            except Exception as err:
                handle_error(err)
                continue



# region utylities
def get_current_proxy(proxies, proxy_index):
    if len(proxies) == 0:
        current_proxy = {}
    else:
        proxy_parts = proxies[proxy_index].split(":")
        ip = ":".join(proxy_parts[:2])
        auth_info = ":".join(proxy_parts[2:])
        current_proxy = {'http': f"http://{auth_info}@{ip}"}
    return current_proxy


def get_items_to_compare(skingg_item_info):
    skingg_item = SkinggItem.get_skingg_item_price_name_id(skingg_item_info)
    steam_item = SteamItem(skingg_item.name)
    return skingg_item, steam_item


def purchase_item_if_necessary(brute_force_mode, file, item_list, skingg_item, steam_item):
    if should_purchase_item(steam_item, skingg_item, brute_force_mode, item_list):
        print("берем")
        with open("buy_me.txt", "a", encoding="utf-8") as to_buy_file:
            to_buy_file.write(f"https://skinout.gg/en/market/{urllib.parse.quote(skingg_item.id_name, safe=':/')}\n"
                              f"https://steamcommunity.com/market/listings/730/{urllib.parse.quote(steam_item.name, safe=':/')}\n"
                              "---------------------------------------------------------------------------\n")
        putchase_logger(file, skingg_item, steam_item)
        # Purchaser.purchase_all_items(skingg_item.id_name, steam_item.price, auth_data, proxy)


def handle_error(err):
    error_logger(err)
    initiativ.release()
    time.sleep(5)


def error_logger(err):
    traceback_str = traceback.format_exc()
    print(f"ОШИБКА! {err} ||| {traceback_str}")

    with open("error_log.txt", "a", encoding="utf-8") as error:
        error.write(f"ОШИБКА! {err} ||| {traceback_str}\n   {time.localtime()}\n")


def await_and_rerun(brute_force_mode, delay, proxies, skingg_page, skingg_page_count):
    skingg_page += 1
    if skingg_page > skingg_page_count:
        print("все странички были проверены")
        time.sleep(delay)
        main(brute_force_mode, proxies)
    initiativ.release()
    return skingg_page


def swap_proxy_if_necessary(index, proxies, proxy_index):
    if index % 20 == 0 and index > 0:
        return (proxy_index + 1) % len(proxies)
    else:
        return 0


def putchase_logger(file, skingg_item, steam_item):
    print(skingg_item.id_name, steam_item.price, skingg_item.price)
    file.write(f"шмотка: {skingg_item.name} - {time.localtime().tm_hour}:{time.localtime().tm_min}\n")

# endregion

# region multytread


def auth_threader():
    while True:
        initiativ.acquire()
        global auth_data
        auth_data = make_auth(CONFIG.login, CONFIG.password, CONFIG.shared_secret)
        initiativ.release()
        time.sleep(86400)


auth_thread = threading.Thread(target=auth_threader)
main_tread = threading.Thread(target=main, args=(CONFIG.brute_force_mode, CONFIG.proxies))
initiativ = threading.Lock()

auth_data = AuthData('', '')

# auth_thread.start()
# time.sleep(1)
main_tread.start()

# endregion



