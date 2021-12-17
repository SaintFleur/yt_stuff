"""
    Holds the logic for editing maps.
    Generating new maps and play testing.
    Saving and validating maps
    """
from utils import Colors
import pygame

class MapMaker:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.color = Colors.Color()



    def on_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.mod and pygame.K_ESCAPE:
                self.running = False
        pass

    def loop(self):
        self.running = True
        print("Hello")

        while self.running:
            self.window.fill(self.color.background)
            for event in pygame.event.get():
                self.on_event(event)



            pygame.display.update()
        # handle the game loop here
        pass
