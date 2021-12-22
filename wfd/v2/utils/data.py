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
class Space_Names:
    def __init__(self):
        self.name_map = {
        Space_Type.EMPTY : "Empty",
        Space_Type.GRASS : "Grass",
        Space_Type.PATH  : "Path",
        Space_Type.TOWER : "Tower", #will probably need to change to holding cell
        Space_Type.START : "Start",
        Space_Type.END   : "End"
        }
