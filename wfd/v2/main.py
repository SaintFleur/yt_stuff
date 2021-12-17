"""starting point for the game"""
import pygame
from utils import Colors
from utils import Button
from utils import GameState

# boiler plate pygame stuff
screen_size = (1920, 1080)
clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("WFD v2")
window = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
color = Colors.Color()
play_button = Button.Button(Button.Type.MENU, (960, 180), "PLAY")
mapmaker_button = Button.Button(Button.Type.MENU, (960, 540), "MAP MAKER")
settings_button = Button.Button(Button.Type.MENU, (960, 900), "SETTINGS")
state = GameState.State.MAIN_MENU

def on_event(event):
    # handle events
    if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
        if event.mod and pygame.K_ESCAPE:
            print("Exiting")
            close_gracefully()
    pass

def close_gracefully():
    pygame.quit()
    quit()

while True:
    for event in pygame.event.get():
        window.fill(color.background)
        on_event(event)

        if state == GameState.State.MAIN_MENU:
            play_button.draw(pygame, window)
            mapmaker_button.draw(pygame, window)
            settings_button.draw(pygame, window)

        pygame.display.update()
