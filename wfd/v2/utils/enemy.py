"""Holds enemy prefabs for now basic logic"""
from enum import Enum
import pygame

class enemy_type(Enum):
    PAWN = 0
    TANK = 1
    SPEED = 3
# Need to get the PFP of the player sending the enemy that could be really cool

class Enemy:
    def __init__(self, pos, pathing_list, grid):
        self.health = 10
        self.starting_health = 10
        self.speed = 1
        self.position = pos
        self.pathing_list = pathing_list # list of next grid space to visit
        self.size = (40,40)
        self.grid = grid

    def draw(self, window):
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

        window.blit(cropped_pic, (self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2))

    def move(self):
        target_pos = self.grid[self.pathing_list[0][0]][self.pathing_list[0][1]]["rect"].center

        if self.position[0] < target_pos[0]:
            self.position = (self.position[0] + 1, self.position[1])

        if self.position[1] < target_pos[1]:
            self.position = (self.position[0], self.position[1] + 1)

        if self.position[0] > target_pos[0]:
            self.position = (self.position[0] - 1, self.position[1])

        if self.position[1] > target_pos[1]:
            self.position = (self.position[0], self.position[1] - 1)

        if target_pos == self.position:
            self.pathing_list.pop(0)
