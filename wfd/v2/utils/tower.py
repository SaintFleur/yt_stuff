"""will hold the tower logic"""
from enum import Enum
import math
import pygame.gfxdraw as pygfx
from utils import Colors
class tower:
    def __init__(self, position):
        self.level = 0
        self.damage = 1
        self.hit_speed = 1  #1 damage per second
        self.position = position
        self.last_attack = 0
        self.range = 3
        self.enemie_destroyed = 0

    def attack(self, enemy_list, map_factor, window, ticks):
        tracked_enemy = None

        translated_range = self.range * map_factor
        translated_position = (int(self.position[0] * map_factor + (map_factor - 1)/2), int(self.position[1] * map_factor + (map_factor - 1)/2))

        for enemy in enemy_list:
            if math.dist(translated_position, enemy.position) <= translated_range and enemy.health > 0:
                if tracked_enemy:
                    if len(enemy.pathing_list) <= len(tracked_enemy.pathing_list):
                        if enemy.distance_to_next_target_pos < tracked_enemy.distance_to_next_target_pos:
                            tracked_enemy = enemy
                else:
                        tracked_enemy = enemy

        if tracked_enemy:
            tracked_enemy.health -= self.damage
            if tracked_enemy.health == 0:
                self.enemie_destroyed += 1
            self.last_attack = ticks


    def draw_range(self, map_factor, window):
        translated_range = self.range * map_factor
        translated_position = (int(self.position[0] * map_factor + (map_factor - 1)/2), int(self.position[1] * map_factor + (map_factor - 1)/2))
        pygfx.aacircle(window,*translated_position, translated_range, Colors.Color().health_red)
    # place_holders
    # not using them now but some good options for later

    def level_up(self):
        pass
        
    def closest_targeting(self):
        pass

    def furthest_along_targeting(self):
        pass

    def highest_health_targeting(self):
        pass

    def lowest_health_targeting(self):
        pass
