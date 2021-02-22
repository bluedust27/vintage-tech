from __future__ import annotations
from typing import List
import datetime


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
        Collectible.TYPE_LIST.append("All")
        for c in Collectible.COLLECTIBLE_LIST:
            if c.type not in Collectible.TYPE_LIST:
                Collectible.TYPE_LIST.append(c.type)



    @staticmethod
    def __get_date_now(cls):
        pass

