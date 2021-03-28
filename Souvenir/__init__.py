from __future__ import annotations

import os
import uuid
from typing import List
import datetime
import jsonpickle


class Collectible:
    COLLECTIBLE_LIST: List[Collectible] = []
    TYPE_LIST: List[str] = []
    TYPE_LIST_DISPLAY: List[str] = []

    def __init__(self, name, c_type, date_manufactured, date_added, description, uid):

        self.name: str = name
        self.type: str = c_type
        self.date_manufactured: datetime.date = date_manufactured
        self.date_added: datetime.date = date_added
        self.description: str = description
        self.uid: uuid = uid
        Collectible.COLLECTIBLE_LIST.append(self)

    @staticmethod
    def populate_type_list():
        Collectible.TYPE_LIST.clear()
        Collectible.TYPE_LIST.extend(("All", "Computer", "Camera", "Phone", "Video Player"))
        Collectible.load_from_file()
        for c in Collectible.COLLECTIBLE_LIST:
            if c.type not in Collectible.TYPE_LIST:
                Collectible.TYPE_LIST.append(c.type)

    @staticmethod
    def save_to_file() -> None:
        json_object = jsonpickle.encode(Collectible.COLLECTIBLE_LIST, unpicklable=False)
        with open('collectibles.json', 'w') as outfile:
            outfile.write(json_object)

    @staticmethod
    def load_from_file() -> None:
        Collectible.COLLECTIBLE_LIST.clear()

        if not os.path.isfile('collectibles.json') or not os.path.getsize('collectibles.json') > 0:
            return

        with open('collectibles.json') as infile:
            json_object = infile.read()
            list_of_dict = jsonpickle.decode(json_object)
            for item in list_of_dict:
                Collectible(item["name"],
                            item["type"],
                            datetime.datetime.strptime(item['date_manufactured'], '%Y-%m-%d').date(),
                            datetime.datetime.strptime(item['date_added'], '%Y-%m-%d').date(),
                            item["description"],
                            item["uid"])

    @staticmethod
    def populate_type_list_display():
        Collectible.TYPE_LIST_DISPLAY.clear()
        Collectible.TYPE_LIST_DISPLAY.append("All")
        Collectible.load_from_file()
        for c in Collectible.COLLECTIBLE_LIST:
            if c.type not in Collectible.TYPE_LIST_DISPLAY:
                Collectible.TYPE_LIST_DISPLAY.append(c.type)
