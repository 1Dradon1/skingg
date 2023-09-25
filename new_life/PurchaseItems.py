import time
from validate_cheap_item import ComparePrices
from get_info_form_skingg import ItemParser
import requests
import json
from auth_data import AuthData


class Purchaser:
    @staticmethod
    def purchase_item(item_id: str, auth_data: AuthData):
        Purchaser._add_item_to_market_cart(item_id, auth_data)
        Purchaser._buy_cart(auth_data)
        print("purchased")
        time.sleep(3)

    @staticmethod
    def purchase_all_items(skingg_item_name_id: str, steam_price: float, auth_data: AuthData, proxy):
        item = ItemParser.get_skingg_item(skingg_item_name_id, proxy)
        if ComparePrices(steam_price, item.price):
            Purchaser.purchase_item(item.item_id, auth_data)
            Purchaser.purchase_all_items(skingg_item_name_id, steam_price, auth_data)

    @staticmethod
    def _add_item_to_market_cart(item_id: str, auth_data: AuthData):
        data = {
            'id': item_id,
            'token': auth_data.token
        }
        saved_cookies = {
            'PHPSESSID': auth_data.phpsessid_cookie
        }

        response = requests.post("https://skinout.gg/api/market/cart/add", data=json.dumps(data), cookies=saved_cookies)
        return response

    @staticmethod
    def _buy_cart(auth_data: AuthData):
        data = {
            'token': auth_data.token
        }
        saved_cookies = {
            'PHPSESSID': auth_data.phpsessid_cookie
        }

        response = requests.post("https://skinout.gg/api/market/cart/buy", data=json.dumps(data), cookies=saved_cookies)
        return response
