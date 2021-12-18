"""starting point for the game"""
import pygame
from utils import Colors
from utils import Button
from utils import GameState
from mapmaker import map_maker

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

menu_buttons = {
    "play" : play_button.draw(window),
    "mapmaker" : mapmaker_button.draw(window),
    "settings" : settings_button.draw(window)
    }

#state is used to track what the game is doing
state = GameState.State.MAIN_MENU

def draw_menu_buttons():
    menu_buttons = {
        "play" : play_button.draw(window),
        "mapmaker" : mapmaker_button.draw(window),
        "settings" : settings_button.draw(window)
        }



def on_event(event):
    global state
    # handle events
    if event.type == pygame.KEYUP:
        if event.mod and pygame.K_ESCAPE:
            print("Exiting")
            close_gracefully()

    if event.type == pygame.MOUSEBUTTONDOWN:
        # will probably want to add a mousebuttonup validator to do the action
        #can add clicked animation here
        x,y = event.pos
        for key in menu_buttons:
            if menu_buttons[key].collidepoint(x, y):
                if key == "play":
                    state = GameState.State.PLAY
                elif key == "mapmaker":
                    state = GameState.State.MAP_MAKER
                elif key == "settings":
                    state = GameState.State.SETTINGS

def close_gracefully():
    pygame.quit()
    quit()

while True:
    window.fill(color.background)
    for event in pygame.event.get():
        on_event(event)

    if state == GameState.State.MAIN_MENU:
        print("MAIN_MENU")
        draw_menu_buttons()
    elif state == GameState.State.MAP_MAKER:
        print("hello")
        map_maker.MapMaker(window).loop()
        pygame.event.get()
    else:
        print("There is nothing")

    pygame.display.update()
    state = GameState.State.MAIN_MENU
