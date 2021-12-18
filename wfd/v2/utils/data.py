""""Holds the data objects such as enemies and towers"""
from dataclasses import dataclass
from enum import Enum

class Space_Type(Enum):
    EMPTY = 0
    GRASS = 1
    PATH  = 2
    TOWER = 3
    START = 4
    END   = 5

    def next(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) + 1
        if index >= len(members):
            # to cycle around
            index = 0
            #
            # to error out
            # raise StopIteration('end of enumeration reached')
        return members[index]

    def prev(self):
        cls = self.__class__
        members = list(cls)
        index = members.index(self) - 1
        if index < 0:
            # to cycle around
            index = len(members) - 1
            #
            # to error out
            #raise StopIteration('beginning of enumeration reached')
        return members[index]

class Space_Colors:
    def __init__(self):
        self.color_map = {
            Space_Type.EMPTY : (255,255,255),
            Space_Type.GRASS : (69,70,42),
            Space_Type.PATH  : (249,237,204),
            Space_Type.TOWER : (87,98,213),
            Space_Type.START : (239,39,166),
            Space_Type.END   : (255,34,12)

        }
