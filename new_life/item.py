import json
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
        self.price = 100000.0

    def get_steam_price_by_name(self):
        response = requests.get(
            f"https://steamcommunity.com/market/priceoverview/?market_hash_name={self.name}&appid=730&currency=1")
        time.sleep(CONFIG.steam_parsing_delay)
        price = float(response.json()['median_price'][1:])
        self.price = price

    '''
        class Item:
            def __init__(self, default_name: str, id_name: str, id: str, price: float):
                self.name = default_name
                self.id_name = id_name
                self.id = id
                self.price = price

        @staticmethod
        def get_skingg_item_price_name_id(cheapest_item: dict) -> 'Skingg.Item':
            return Skingg.Item(
                default_name=cheapest_item['name'],
                id_name=cheapest_item['name_id'],
                id=cheapest_item['id'],
                price=float(cheapest_item['price'])
            )
    '''