import re
import time
import requests
from config import CONFIG


class Item:
    pass


class SkinggItem(Item):
    def __init__(self, default_name: str, id_name: str, item_id: str, price: float):
        self.name = default_name
        self.id_name = id_name
        self.item_id = item_id
        self.price = price

    @classmethod
    def get_skingg_item_price_name_id(cls, item_data: dict) -> 'SkinggItem':
        return cls(
            default_name=item_data['name'],
            id_name=item_data['name_id'],
            item_id=item_data['id'],
            price=float(item_data['price'])
        )




class SteamItem(Item):
    def __init__(self, name: str):
        self.name = name.replace("&", "%26")
        self.price = 0.0

    def get_steam_price_by_name(self):
        response = requests.get(
            f"https://steamcommunity.com/market/priceoverview/?market_hash_name={self.name}&appid=730&currency=1")
        time.sleep(CONFIG.steam_parsing_delay)

        parsed_response = response.json()
        if 'median_price' in parsed_response:
            price = float(parsed_response['median_price'][1:])
            self.price = price
        else:
            self.price = 0.0


