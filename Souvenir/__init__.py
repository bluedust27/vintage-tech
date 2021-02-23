from __future__ import annotations

import os
from typing import List
import datetime
import jsonpickle


class Collectible:
    COLLECTIBLE_LIST: List[Collectible] = []
    TYPE_LIST: List[str] = []

    def __init__(self, name, c_type, date_manufactured, date_added, description):
        self.name: str = name
        self.type: str = c_type
        self.date_manufactured: datetime = date_manufactured
        self.date_added: datetime = date_added
        self.description: str = description
        Collectible.COLLECTIBLE_LIST.append(self)

    @staticmethod
    def populate_type():
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
                            item["date_manufactured"],
                            item["date_added"],
                            item["description"])
