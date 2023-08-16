import json
import re

import requests
from item import SkinggItem


def request_skingg_page_info(page: str, sort_by: str, hold: str) -> dict:
    """

    Parameters
    ----------
    page
        номер странички
    sort_by
        тип сортировки дефолт popularity_desc
    hold
        задержка обмена

    Returns
    -------
    Notes
    -------
        cart_sum: "0.00"\n
        currency: "usd"\n
        currency_symbol: "$"\n
        items: [,…]\n

    """

    response = requests.get(f"https://skinout.gg/api/market/items?page={page}&sort={sort_by}&hold={hold}")

    return response.json()


def parse_data_from_skingg_page(current_page: int, sort_by: str, hold: str) -> tuple[list, int]:
    """

    Parameters
    ----------
    sort_by
    current_page: int
        страничка которую будем парсить

    Notes
    -------
    0: {id: "150762", market_hash_name: "Fracture Case", name: "Fracture Case", name_id: "fracture-case",…}
        float: "0"\n
        id: "150762"\n
        img: "https://steamcommunity-a.akamaihd.net/.."\n
        in_cart: false\n
        locked: true\n
        market_hash_name: "Fracture Case"\n
        name: "Fracture Case"\n
        name_id: "fracture-case"\n
        price: "0.46"\n
        stickers: []\n
        total_count: 944\n
        unlock_time: "12 часов"\n
        page: 1\n
        page_count: 41\n
        success: true\n

    Returns
    -------
    tuple[list, str]
        вещи и общее кол-во страниц

    """

    page_data = request_skingg_page_info(str(current_page), sort_by, hold)
    items = page_data['items']
    page_count = page_data['page_count']

    return items, int(page_count)


class ItemParser:
    @staticmethod
    def get_skingg_item_page_info(skingg_item_id: str) -> object:
        data = {
            'name_id': skingg_item_id
        }
        response = requests.post("https://skinout.gg/api/market/item", data=json.dumps(data))
        return response.json()["items"][0]

    @staticmethod
    def get_skingg_item(skingg_item_name_id: str) -> SkinggItem:
        item_info = ItemParser.get_skingg_item_page_info(skingg_item_name_id)
        item = SkinggItem(item_info["name"], item_info["name_id"], item_info["id"], float(item_info["price"]))
        return item


    @staticmethod
    def get_skingg_item_by_name(name: str) -> 'SkinggItem':
        return ItemParser.get_skingg_item(ItemParser.get_name_id_from_default_name(name))

    @staticmethod
    def get_name_id_from_default_name(name: str):
        name_id = re.sub(r'[^a-zA-Z0-9\s-]', '', name)
        name_id = re.sub(r'\s+', '-', name_id)
        name_id = name_id.lower()
        return name_id

