"""
    Holds the logic for editing maps.
    Generating new maps and play testing.
    Saving and validating maps
    """
from utils import Colors, Button, enemy, tower
from utils.data import Space_Type, Space_Colors, Space_Names
import math
import json
import pygame
import copy
import pygame.gfxdraw

class MapMaker:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.color = Colors.Color()
        self.grid_size = 20      #length and width of the grid
        self.rect_size = 50
        self.grid_padding = 2
        self.grid = {}
        self.path = []
        self.pixel_path = []
        self.pixel_path_total = 0
        # shouldn't be hard coded
        self.start = (0,9)
        self.end = ()
        self.towers = []

        # going to need to change this into it's own controller that can receive signals
        self.last_spawn = 0
        self.enemies = []

        self.slb_buttons = {
            "save" : {
                "button" : Button.Button(Button.Type.MAP_MAKER_SLB, (1200, 880), "SAVE"),
                "rect": None},
            "back" : {
                "button" : Button.Button(Button.Type.MAP_MAKER_SLB,(1450, 880), "BACK"),
                "rect": None
                },
            "load" : {
                "button" : Button.Button(Button.Type.MAP_MAKER_SLB, (1700, 880), "LOAD"),
                "rect": None
                }, #add clear pause and simulate button
            }

        self.last_ten_frame_rates = []

        self.selected = None #will be able to select square and give options for what to do
        self.clock = pygame.time.Clock()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.mod and pygame.K_ESCAPE:
                self.running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #check if one of the slb buttons was pressed
            for key in self.slb_buttons:
                if self.slb_buttons[key]["rect"].collidepoint(pygame.mouse.get_pos()):
                    if key == "back":
                        self.running = False
                    if key == "save":
                        self.save_map()
                    if key == "load":
                        print("LOADING......")
                        self.load_map()

            #check if grid was pressed
            grid_space_selected = False
            for i_key in self.grid:
                for j_key in self.grid:
                    if self.grid[i_key][j_key]["rect"].collidepoint(pygame.mouse.get_pos()):
                        if self.selected == (i_key, j_key):

                            #self.grid[i_key][j_key]["type"] += 1
                            self.selected = (i_key, j_key) # need to change this into a selectable python object
                            temp_list = list(Space_Type)
                            i = temp_list.index(self.grid[i_key][j_key]["type"])
                            if i == len(temp_list) - 1:
                                self.grid[i_key][j_key]["type"] = temp_list[0]
                            else:
                                self.grid[i_key][j_key]["type"] = temp_list[ i + 1]

                        grid_space_selected = True
                        self.selected = (i_key, j_key)

            if not grid_space_selected:
                self.selected = None

    def load_map(self):
        with open("maps/data.json", 'r') as f:
            self.grid = json.load(f)

        self.grid = {int(k):v for k,v in self.grid.items()}

        for key in self.grid.keys():
            self.grid[key] = {int(k):v for k,v in self.grid[key].items()}

        for i_key in self.grid:
            for j_key in self.grid[i_key]:
                 self.grid[i_key][j_key]["type"] = list(Space_Type)[self.grid[i_key][j_key]["type"]]

        self.draw_map()

    def draw_map(self):
        for i_key in self.grid.keys():
            for j_key in self.grid[i_key].keys():
                pos = self.to_coord(self.grid[i_key][j_key]["position"])
                self.grid[i_key][j_key]["rect"] = pygame.draw.rect(self.window,
                                                                Space_Colors().color_map[self.grid[i_key][j_key]["type"]],
                                                                (pos[0], pos[1], self.rect_size,self.rect_size))

    def generate_map(self):
        for i in range(self.grid_size):
            if i not in self.grid.keys():
                i_coord = (self.grid_padding * (i + 1) + (self.rect_size * i))
                self.grid[i] = {}
            for j in range(self.grid_size):
                j_coord = (self.grid_padding * (j + 1) + (self.rect_size * j))
                rect = pygame.draw.rect(self.window, Space_Colors().color_map[Space_Type.EMPTY],(i_coord, j_coord, self.rect_size, self.rect_size) )

                self.grid[i][j] = {
                    "rect" : rect,
                    "type" : Space_Type.EMPTY,
                    "position": (i, j)
                    }

    def generate_random_path(self):
        pass

    def save_map(self):
        temp_grid = copy.deepcopy(self.grid)
        for i_key in temp_grid:
            for j_key in temp_grid[i_key]:
                temp_grid[i_key][j_key]["type"] = self.grid[i_key][j_key]["type"].value
                temp_grid[i_key][j_key]["rect"] = None

        with open("maps/data.json", 'w') as file:
            json.dump(temp_grid, file)

    def to_coord(self, coords):
        # turn a cell into the corresponding pixel position
        i_coord = (self.grid_padding * (coords[0] + 1) + (self.rect_size * coords[0]))

        j_coord = (self.grid_padding * (coords[1] + 1) + (self.rect_size * coords[1]))

        return (i_coord, j_coord)

    def draw_buttons(self):
        for key in self.slb_buttons.keys():
            self.slb_buttons[key]["rect"] = self.slb_buttons[key]["button"].draw(self.window)

    def draw_selected_info(self):
        # draw the selected grid
        size = (750, 400)
        pos = (1100, 25)
        bounding_rect = pygame.draw.rect(self.window, Colors.Color().white, (pos[0], pos[1], size[0], size[1]))

        pygame.draw.rect(self.window,
            Space_Colors().color_map[self.grid[self.selected[0]][self.selected[1]]["type"]],
            (pos[0]  + 10, pos[1] + 10, size[1] - 20, size[1] - 20))



        space_name_rect = pygame.draw.rect(
            self.window,
            Colors.Color().title,
            (pos[0] + 400, pos[1] + 10, 340, 40))


        space_name = Space_Names().name_map[self.grid[self.selected[0]][self.selected[1]]["type"]] + " " + str(self.selected)

        font = pygame.font.SysFont('chalkduster.ttf', 30)
        text = font.render(space_name, True, (255, 255, 255))
        self.window.blit(text, text.get_rect(center = space_name_rect.center))

        grid_options = []

        for i in range(len(list(Space_Type))):

            pass

        # TODO: deselect
        # TODO: brushes, being able to paint the path

    def check_neighbours(self, pos, visited):

        pass

    def in_map(self, pos):
        if pos[0] < 0 or pos[1] < 0 or pos[0] > self.grid_size - 1 or pos[1] > self.grid_size - 1:
            return False
        return True

    def solve_map(self):
        # For now only solve for one path
        # TODO: Make more robust handle invalid maps

        end_not_found = True

        visited = [self.start]

        to_check = [self.start]

        self.path.append(self.start)

        while end_not_found:
            checking = to_check.pop(0)
            visited.append(checking)

            if self.grid[checking[0]][checking[1]]["type"] == Space_Type.END:
                self.path.append(checking)
                end_not_found = False
            else:
                left = (checking[0] - 1 , checking[1])
                right = (checking[0] + 1, checking[1])
                down = (checking[0] , checking[1] + 1)
                up = (checking[0] , checking[1] - 1)

                if self.in_map(left) and self.grid[left[0]][left[1]]["type"] in (Space_Type.PATH, Space_Type.END) and left not in visited:
                    to_check.append(left)
                    self.path.append(left)
                if self.in_map(right) and self.grid[right[0]][right[1]]["type"] in (Space_Type.PATH, Space_Type.END)  and right not in visited:
                    to_check.append(right)
                    self.path.append(right)
                if self.in_map(down) and self.grid[down[0]][down[1]]["type"] in (Space_Type.PATH, Space_Type.END) and down not in visited:
                    to_check.append(down)
                    self.path.append(down)
                if self.in_map(up) and self.grid[up[0]][up[1]]["type"] in (Space_Type.PATH, Space_Type.END) and not up in visited:
                    to_check.append(up)
                    self.path.append(up)


                if len(to_check) == 0 and end_not_found:
                    end_not_found = False
                    print("INVALID MAP")

    def calculate_pixel_path(self):
        # get the center of the starting grid space_name
        # get the center of the next grid_space

        current = self.grid[self.start[0]][self.start[1]]["rect"].center

        self.pixel_path = [current]

        for i in range(1,len(self.path)):
            target = self.grid[self.path[i][0]][self.path[i][1]]["rect"].center
            print("Delimenator: " + str(i))
            print(self.path[i])
            if i == 3 :
                print("Current: " + str(current))
                print("Target: " + str(target))
            while target[0] !=  current[0] or target[1] != current[1]:
                if i == 3 :
                    print("Current: " + str(current))
                    print("Target: " + str(target))
                if  target[0] > current[0]:
                    current = (current[0] + 1, current[1])
                    self.pixel_path.append(current)
                if  current[1] < target[1]:
                    current = (current[0], current[1] + 1)
                    self.pixel_path.append(current)
                if  target[0] < current[0]:
                    current = (current[0] - 1, current[1])
                    self.pixel_path.append(current)
                if  current[1] > target[1]:
                    current = (current[0], current[1] - 1)
                    #print(current)
                    self.pixel_path.append(current)

        self.pixel_path_total = len(self.pixel_path)

    def locate_towers(self):
        for i_key in self.grid:
            for j_key in self.grid[i_key]:
                if self.grid[i_key][j_key]["type"] == Space_Type.TOWER:
                    self.towers.append(tower.tower((i_key, j_key)))

    def spawn_enemy(self):
        self.enemies.append(enemy.Enemy(self.grid[self.start[0]][self.start[1]]["rect"].center, self.path[1:], self.grid, pygame.time.get_ticks()))

    def loop(self):
        self.running = True
        self.generate_map()
        self.load_map()
        self.solve_map()
        self.calculate_pixel_path()

        self.spawn_enemy()

        last_hit = pygame.time.get_ticks()

        self.locate_towers()
        while self.running:

            time = pygame.time.get_ticks()
            self.clock.tick()

            self.last_ten_frame_rates.append(self.clock.get_fps())
            if len(self.last_ten_frame_rates) > 10:
                self.last_ten_frame_rates.pop(0)

            #print("Average Frame Rate: " + str(sum(self.last_ten_frame_rates)/10))

            self.window.fill(self.color.background)
            for event in pygame.event.get():
                self.on_event(event)

            self.draw_buttons()

            self.draw_map()
            for enem in self.enemies:
                enem.move(self.pixel_path)
                enem.draw(self.window)
                if enem.health <= 0:
                    self.enemies.remove(enem)
                if enem.pos_index == self.pixel_path_total:
                    self.enemies.remove(enem)

            for tow in self.towers:
                if time - tow.last_attack >= tow.hit_speed * 1000:
                    tow.attack(self.enemies, self.rect_size + self.grid_padding, self.window, time)
                    tow.draw_range(self.rect_size + self.grid_padding, self.window)

            if time - self.last_spawn > 500 and len(self.enemies) < 1:
                self.spawn_enemy()
                self.last_spawn = time

            for _ in self.pixel_path:
                pygame.gfxdraw.pixel(self.window, *_, Colors.Color().health_green)

            if self.selected:
                self.draw_selected_info()

            pygame.display.update()
        #next is the tower logic
