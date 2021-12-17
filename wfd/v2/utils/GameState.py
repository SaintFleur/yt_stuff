"""Enum for what state the game is in"""
from enum import Enum

class State(Enum):
    MAIN_MENU = 1
    PLAY = 2
    MAPMAKER = 3
    PAUSED = 4
