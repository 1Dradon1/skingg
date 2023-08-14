import time
from new_life.validate_cheap_item import should_purchase_item, get_item_list
from get_info_form_skingg import *
from item import SkinggItem, SteamItem
from PurchaseItems import Purchaser
from auth import make_auth
from config import CONFIG


def brute_force(brute_force_mode):
    skingg_page = CONFIG.skingg_page
    item_list = get_item_list()
    auth_data = make_auth(CONFIG.login, CONFIG.password, CONFIG.shared_secret)
    with open("item_buy_log.txt", "a") as file:
        while True:
            try:
                print("страничка" + skingg_page)
                skingg_page_items, skingg_page_count = parse_data_from_skingg_page(skingg_page, CONFIG.sort_by, CONFIG.hold)

                for skingg_item_info in skingg_page_items:
                    skingg_item = SkinggItem.get_skingg_item_price_name_id(skingg_item_info)
                    steam_item = SteamItem(skingg_item.name)
                    steam_item.get_steam_price_by_name()

                    if should_purchase_item(steam_item, skingg_item, brute_force_mode, item_list):
                        print(skingg_item.id_name, steam_item.price, skingg_item.price)
                        file.write(f"шмотка: {skingg_item.name}\n    {time.localtime()}")

                        Purchaser.purchase_all_items(skingg_item.id_name, steam_item.price, auth_data)

                skingg_page += 1

                if 0 <= time.localtime().tm_hour < 2:
                    auth_data = make_auth(CONFIG.login, CONFIG.password, CONFIG.shared_secret)

                if skingg_page > skingg_page_count:
                    print("все странички были проверены")
                    brute_force(brute_force_mode)

            except Exception as err:
                print(f"ОШИБКА! {err}")
                with open("error_log.txt", "a") as error:
                    error.write(f"ОШИБКА! {err}\n    {time.localtime()}")
                time.sleep(360)
                continue


brute_force()