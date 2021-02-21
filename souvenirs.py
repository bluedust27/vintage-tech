from __future__ import annotations
from typing import List
import datetime


class Collectibles:
    COLLECTIBLES_LIST: List[Collectibles] = []

    def __init__(self, name, c_type, date_manufactured, description):
       # self.__id = Collectibles.__get_next_id()
        self.name: str = name
        self.type: list = c_type
        # self.__date_added = Collectibles.__get_date_now()
        self.date_manufactured: datetime = date_manufactured
        self.description: str = description
        Collectibles.COLLECTIBLES_LIST.append(self)

    @staticmethod
    def __get_next_id(cls):
        pass

    @staticmethod
    def __get_date_now(cls):
        pass

