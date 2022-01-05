"""This is for previewing clickable items"""

from utils.Colors import Color
from utils.data import Space_Type, Space_Colors, Space_Names
import pygame

class Preview:
    def __init__(self, window):

        # holder
        self.window = window

        self.width = 750
        self.height = 400
        self.position = (1100, 25)

        self.padding = 10

        self.rect = self.initialize()

        # title
        self.title_height = 40
        self.title_width = 340
        self.title_rect = self.draw_title()

    def initialize(self):
        pygame.draw.rect(self.window, Color().white, (*self.position, self.width, self.height))

    def draw_title(self, ):
        pygame.draw.rect(self.window, Color().title, (self.position[0] + 400, self.position[1] + self.padding, self.title_width, self.title_height))

    def draw_space(self, space_type):
        space_name =
        pass

    def draw_tower(self):
        pass

    def draw_enemy(self):
        pass
