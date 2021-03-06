"""Holds enemy prefabs for now basic logic"""
from enum import Enum
import pygame
from utils import Colors
import math

class enemy_type(Enum):
    PAWN = 0
    TANK = 1
    SPEED = 3
# Need to get the PFP of the player sending the enemy that could be really cool

class Enemy:
    def __init__(self, pos, pathing_list, grid, time):
        self.health = 20
        self.starting_health = 20
        self.speed = 1 # one grid space a second
        self.pathing_list = pathing_list # list of next grid space to visit
        self.size = (35,35)
        self.grid = grid
        self.position = pos
        self.pos_index = 0
        self.distance_to_next_target_pos = 0
        self.img = self.create_img()

        #time based movement stuff



    def create_img(self):
        pic = pygame.image.load("resources/images/mxc_pfp.png")
        pic = pygame.transform.scale(pic, self.size)

        #---------------------------------------------------
        #First create acircle that only shows what you don't want
        image = pygame.Surface(self.size)
        image.fill((255, 255, 255))
        image.set_colorkey((0, 0, 0))
        pygame.draw.circle(image, (0, 0, 0), (self.size[0]/2, self.size[1]/2), self.size[0]/2)

        #---------------------------------------------
        # use what you don't want as the color key
        cropped_pic = pygame.Surface(self.size, pygame.SRCALPHA)
        cropped_pic.set_colorkey((255,255,255))
        cropped_pic.blit(pic, (0,0))
        cropped_pic.blit(image, (0,0))

        return cropped_pic


    def draw(self, window):
        position = self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2


        window.blit(self.img, position)

        # health bar : simpler than I thought but may need to increase logic
        health_percent = self.health / self.starting_health
        pygame.draw.rect(window, Colors.Color().health_red, (position[0] , position[1] + 37, self.size[0], 4 ))
        pygame.draw.rect(window, Colors.Color().health_green, (position[0] , position[1] + 37, self.size[0] * health_percent, 4 ))



    def move(self, pixel_list):
        #very complicated but it's easier to calculate every position needed to move and just move it there in time over time increments
        self.pos_index += 1
        if self.pos_index < len(pixel_list):
            self.position = pixel_list[self.pos_index]
