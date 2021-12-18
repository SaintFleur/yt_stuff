"""hold the properties of a button"""
from enum import Enum
import utils.Colors as Colors
import pygame

class Type(Enum):
    MENU = 1
    PLAY = 2
    SETTINGS = 3
    MAP_MAKER_SLB = 4 #SLB : SAVE LOAD BACK


class ButtonPrefab:
    def __init__(self):
        self.button_map = {
        Type.MENU : {
            "size"   : (800, 150),
            "color"  : Colors.Color().button,
            "sprite" : None  },
        Type.PLAY : {},
        Type.MAP_MAKER_SLB : {
            "size"   : (200, 150),
            "color"  : Colors.Color().button,
            "sprite" : None},
        }

prefab = ButtonPrefab()
class Button:
    def __init__(self, type, position, text):
        self.text = text
        self.size = prefab.button_map[type]["size"]
        self.color = prefab.button_map[type]["color"]
        #have to adjust for button size
        self.position = (position[0] - self.size[0]/2, position[1] - self.size[1] / 2)
        self.sprite = None

    def draw(self, window):
        rect = pygame.draw.rect(window, self.color, (self.position[0], self.position[1], self.size[0],self.size[1]))
        font = pygame.font.SysFont('chalkduster.ttf', 72)
        text = font.render(self.text, True, (255,255,255))
        window.blit(text, text.get_rect(center = rect.center))
        return rect
