from __future__ import annotations
from typing import List
import datetime


class Collectible:
    COLLECTIBLE_LIST: List[Collectible] = []

    def __init__(self, name, c_type, date_manufactured, date_added, description):
       # self.__id = Collectibles.__get_next_id()
        self.name: str = name
        self.type: list = c_type
        self.date_manufactured: datetime = date_manufactured
        self.date_added: datetime = date_added
        self.description: str = description
        Collectible.COLLECTIBLE_LIST.append(self)

    @staticmethod
    def __get_next_id(cls):
        pass

    @staticmethod
    def __get_date_now(cls):
        pass

