"""Created by xirosum for entertainment purposes"""

import pygame
import json
import math

class Enemy:
    def __init__(self, position, next_block):
        self.starting_health = 10
        self.health = 10              # hp
        self.color = (255,0,0)        # color the enemy uses to spawn may use different colors for different types
        self.position = position      # current position
        self.size = 7                 # may have the size change with health
        self.speed = 1                # units per second
        self.next_block = next_block  # used for path finding
        self.last_moved = 0

class Tower:
    def __init__(self, position):
        self.strength = 1        # damage per hit
        self.range = 3           # 3 in game units range
        self.speed = 1000        # one attack per second
        self.position = position
        self.last_fired = 0
        self.enemy_in_range = False
        self.enemies_in_range = []


class App:
     def __init__(self):
         self._running = True
         self.window = None
         self.window_size = self.width, self.height = 600, 600
         self.clock = pygame.time.Clock()

         self.grid_size = 20
         self.rect_size = 25
         self.grid_padding = 1
         self.grid = {}
         self.path = []

         # utilities
         self.colors = {
         0 : (255,255,255), # white
         1 : (255,0,0),     # red
         2 : (0,255,0),     # green
         3 : (0,0,255),     # blue
         4 : (177,52,235),  # purple
         5 : (255,215,0),   # gold
         }

         self.color_map = {
         0 : "nothing",
         1 : "enemy",
         2 : "path",
         3 : "tower",
         4 : "start",
         5 : "end",
         }


         self.start = (-1,-1)
         self.end = (-1,-1)


         # enemy logic
         self.enemy_logic = {
         "last spawned" : 0,
         "enemies" : [] ,
         "spawn timer" : 3000, #in milliseconds
         }

         self.tick_speed = 100
         self.last_tick = 0

         # tower logic
         self.towers = []

     def on_init(self):
         pygame.init()
         pygame.display.set_caption("WFD")
         self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
         self._running = True
         #self.generate_map()
         self.load_map()
         self.initialize_map_objs()
         self.find_path()

     def to_coordinate(self, x, y):
         x = (x * self.rect_size) + x + (self.rect_size / 2) + 1
         y = (y * self.rect_size) + y + (self.rect_size / 2) + 1
         return x,y

     def generate_map(self):
         rect_size = 25
         self.grid_padding = 1

         for i in range(self.grid_size):
             x_coord = (self.grid_padding * (i+1) + (rect_size * i))
             if i not in self.grid.keys():
                 self.grid[i] = {}
             for j in range(self.grid_size):
                 y_coord = (self.grid_padding * (j+1) + (rect_size * j))
                 rect = pygame.draw.rect(self.window, (255,255,255), (x_coord,y_coord,rect_size, rect_size))

                 quit = False

                 if i == 19 and j == 19:
                     quit = True

                 self.grid[i][j] = {
                 "rect" : rect,
                 "color" : (255,255,255),
                 "type" : 0,
                 "quit" : quit
                 }

     def load_map(self):
         #load map from previous save state can add ability to add maps later
         self.generate_map()
         pass
         with open('map_one.txt', 'r') as f:
             self.grid = json.load(f)

         self.grid = {int(k):v for k,v in self.grid.items()}

         for key in self.grid.keys():
             self.grid[key] = {int(k):v for k,v in self.grid[key].items()}

     def save_map(self):
         #save changes made to the map mainly for testing
         dic = {}
         for i in range(len(self.grid)):
             for j in range(len(self.grid[i])):
                 if i not in dic.keys():
                     dic[i] = {}
                 self.grid[i][j]["rect"] = ""
                 dic[i][j] = self.grid[i][j]

         with open('map_one.txt', 'w') as f:
            json.dump(dic, f)

     def initialize_map_objs(self):
         #get the start and the end and towers/other objs
         for i in self.grid.keys():
             for j in self.grid[i].keys():
                 if self.grid[i][j]["type"] == 4 and self.start == (-1,-1):
                     self.start = (i,j)
                     self.grid[i][j]["color"] = (0,112,9)
                 elif self.grid[i][j]["type"] == 3:
                     #add towers
                     self.towers.append(Tower((i,j)))
                     self.grid[i][j]["color"] = self.colors[3]

         # list comprehension is amazing!
         print([k.position for k in self.towers])

     def calc_in_game_unit(self):
         # one unit is the size of the square + the padding
         # locations are calculated from the center of the objs
         return self.rect_size + self.grid_padding

     def find_path(self):
         #find start
         checked = []
         self.end = None
         self.path.append(self.start)

         need_to_visit = [self.start]

         while need_to_visit:
            #solve the maze
            current = need_to_visit.pop(len(need_to_visit)-1)
            checked.append(current)
            #check the top front and bottom and backwards if not in visited
            (current[0] + 1, current[1])

            if current[0] + 1 in self.grid and current[1] in self.grid[0] and (current[0] + 1, current[1]) not in checked:
                 if self.grid[current[0] + 1][current[1]]["type"] == 2:
                     need_to_visit.append((current[0] + 1, current[1]))
                     self.path.append((current[0] + 1, current[1]))
                 if self.grid[current[0] + 1][current[1]]["type"] == 5:
                     self.end = (current[0] + 1, current[1])
            if current[0] - 1 in self.grid and current[1] in self.grid[0] and (current[0] - 1, current[1]) not in checked:
                 if self.grid[current[0] - 1][current[1]]["type"] == 2:
                     need_to_visit.append((current[0] - 1, current[1]))
                     self.path.append((current[0] - 1, current[1]))
                 if self.grid[current[0] - 1][current[1]]["type"] == 5:
                     self.end = (current[0] - 1, current[1])
            if current[0] in self.grid and current[1] + 1 in self.grid[0] and (current[0], current[1] + 1) not in checked:
                 if self.grid[current[0]][current[1] + 1]["type"] == 2:
                     need_to_visit.append((current[0], current[1]+1))
                     self.path.append((current[0], current[1] +1))
                 if self.grid[current[0]][current[1] + 1]["type"] == 5:
                     self.end = (current[0], current[1] + 1)
            if current[0] in self.grid and current[1] - 1 in self.grid[0] and (current[0], current[1] - 1) not in checked:
                 if self.grid[current[0]][current[1] - 1]["type"] == 2:
                     need_to_visit.append((current[0], current[1] - 1))
                     self.path.append((current[0], current[1] - 1))
                 if self.grid[current[0]][current[1] - 1]["type"] == 5:
                     self.end = (current[0], current[1] - 1)

         if self.end != (-1,-1):
             self.path.append(self.end)

         for cell in self.path:
             if  cell != self.start and cell != self.end:
                 self.grid[cell[0]][cell[1]]["color"] = self.colors[2]
                 #print(self.path)

     def spawn_enemy(self):
         # spawn the enemies on a timer and track them
         if pygame.time.get_ticks() - self.enemy_logic["last spawned"] > self.enemy_logic["spawn timer"]:
             enemy = Enemy((self.to_coordinate(self.start[0], self.start[1])), 1)
             pygame.draw.circle(self.window, enemy.color, enemy.position, enemy.size)
             self.enemy_logic["enemies"].append(enemy)
             self.enemy_logic["last spawned"] = pygame.time.get_ticks()

     def move_towards(self, current, target):
         #going to need if we want the enemy to move backwards
         if current[0] < target[0]:
             current = (current[0] + 1, current[1])
         elif current[0] > target[0]:
             current = (current[0] - 1, current[1])
         elif current[1] < target[1]:
             current = (current[0], current[1] + 1)
         elif current[1] > target[1]:
             current = (current[0], current[1] - 1)

         return current

     def move_enemies(self):
         # move enemies through the maze
         count = 0
         for enemy in self.enemy_logic["enemies"]:
             count += 1
             #print(count)
             if pygame.time.get_ticks() - enemy.last_moved > self.tick_speed :
                 next_coordinate = self.to_coordinate(self.path[enemy.next_block][0], self.path[enemy.next_block][1])
                 enemy.position = self.move_towards(enemy.position, next_coordinate)
                 #enemy.circle.move(enemy.position)
                 enemy.last_moved = pygame.time.get_ticks()
                 if enemy.position == self.to_coordinate(self.path[enemy.next_block][0], self.path[enemy.next_block][1]):
                     enemy.next_block += 1
             if enemy.next_block == len(self.path) or enemy.health < 1:
                 self.enemy_logic["enemies"].remove(enemy)
                 #print(len(self.enemy_logic["enemies"]))

             pygame.draw.circle(self.window, enemy.color, enemy.position, enemy.size)

     def tower_action(self):
         #first detect if enemy is in range of the tower

         for tower in self.towers:

             if pygame.time.get_ticks() - tower.last_fired > tower.speed:
                 tower.last_fired = pygame.time.get_ticks()
                 tower.enemies_in_range = []
                 closest_distance = 100000000
                 closest_enemy = None
                 for enemy in self.enemy_logic["enemies"]:
                     #print("Range: " + str(self.calc_in_game_unit() * tower.range))
                     tow_pos = (self.to_coordinate(tower.position[0], tower.position[1]))
                     distance = math.dist(enemy.position, tow_pos)
                     if distance < self.calc_in_game_unit() * tower.range:
                         tower.enemies_in_range.append(enemy)
                         if distance < closest_distance:
                             closest_distance = distance
                             closest_enemy = enemy


                 if len(tower.enemies_in_range) > 0:
                     tower.last_fired = pygame.time.get_ticks()
                     self.grid[tower.position[0]][tower.position[1]]["color"] = (112,112,112)
                     print("Fire!")
                     closest_enemy.health -= tower.strength
                 else:
                     self.grid[tower.position[0]][tower.position[1]]["color"] = self.colors[3]

                     #print(math.dist(enemy.position, tower.position))

     def on_event(self, event):
         if event.type == pygame.QUIT:
             pygame.quit(); exit()

         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
             for x in range(len(self.grid.keys())):
                 for y in range(len(self.grid[x].keys())):
                     rect = self.grid[x][y]["rect"]

                     if rect.collidepoint(pygame.mouse.get_pos()):
                         if self.grid[x][y]["quit"]:
                             self.on_cleanup()
                         self.grid[x][y]["type"] += 1

                         if self.grid[x][y]["type"] > 5:
                             self.grid[x][y]["type"] = 0


                         print(self.color_map[self.grid[x][y]["type"]])

     def on_loop(self):
         pass

     def on_render(self):
         pass

     def on_cleanup(self):
         self.save_map()
         pygame.quit()

     def on_execute(self):
         if self.on_init() == False:
             self._running = False

         background_color = (0,0,0)
         self.window.fill(background_color)

         rect_size = self.rect_size

         for i in range(self.grid_size):
             x_coord = (self.grid_padding * (i+1) + (rect_size * i))
             temp = []
             for j in range(self.grid_size):
                 y_coord = (self.grid_padding * (j+1) + (rect_size * j))
                 rect = pygame.draw.rect(self.window, (255,255,255), (x_coord,y_coord,rect_size, rect_size))
                 self.grid[i][j]["rect"] = rect

         while self._running:
             self.window.fill(background_color)
             events = pygame.event.get()
             for event in events:
                 self.on_event(event)

             for i in range(self.grid_size):
                 x_coord = (self.grid_padding * (i+1) + (rect_size * i))
                 for j in range(self.grid_size):
                     y_coord = (self.grid_padding * (j+1) + (rect_size * j))
                     rect = pygame.draw.rect(self.window, self.grid[i][j]["color"] , (x_coord,y_coord,rect_size, rect_size))

                     self.grid[i][j]["rect"] = rect

             self.move_enemies()
             self.spawn_enemy()
             self.tower_action()
             self.on_loop()
             self.on_render()
             self.clock.tick()
             pygame.display.update()
             print(self.clock.get_fps())


         self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
