"""
    Holds the logic for editing maps.
    Generating new maps and play testing.
    Saving and validating maps
    """
from utils import Colors
from utils import Button
from utils.data import Space_Type, Space_Colors
import pygame

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
        self.start = ()
        self.end = ()
        self.towers = []
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
                }
            }


        self.selected = None #will be able to select square and give options for what to do

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

            #check if grid was pressed
            for i_key in self.grid:
                for j_key in self.grid:
                    if self.grid[i_key][j_key]["rect"].collidepoint(pygame.mouse.get_pos()):
                        #self.grid[i_key][j_key]["type"] += 1
                        temp_list = list(Space_Type)
                        i = temp_list.index(self.grid[i_key][j_key]["type"])
                        if i == len(temp_list) - 1:
                            self.grid[i_key][j_key]["type"] = temp_list[0]
                        else:
                            self.grid[i_key][j_key]["type"] = temp_list[ i + 1]


        pass

    def load_map(self):
        pass

    def generate_map(self):
        for i in range(self.grid_size):
            if i not in self.grid.keys():
                i_coord = (self.grid_padding * (i + 1) + (self.rect_size * i) )
                self.grid[i] = {}
            for j in range(self.grid_size):
                j_coord = (self.grid_padding * (j + 1) + (self.rect_size * j) )
                rect = pygame.draw.rect(self.window, Space_Colors().color_map[Space_Type.EMPTY],(i_coord, j_coord, self.rect_size, self.rect_size) )

                self.grid[i][j] = {
                    "rect" : rect,
                    "type" : Space_Type.EMPTY,
                    "position": (i_coord, j_coord)
                    }

    def save_map(self):
        pass


    def to_coord(self, coords):
        pass


    def draw_buttons(self):
        for key in self.slb_buttons.keys():
            self.slb_buttons[key]["rect"] = self.slb_buttons[key]["button"].draw(self.window)

    def loop(self):
        self.running = True
        print("Hello")
        self.generate_map()
        while self.running:
            self.window.fill(self.color.background)
            for event in pygame.event.get():
                self.on_event(event)

            self.draw_buttons()


            for i_key in self.grid.keys():
                for j_key in self.grid[i_key].keys():
                    pos = self.grid[i_key][j_key]["position"]
                    self.grid[i_key][j_key]["rect"] = pygame.draw.rect(self.window,
                                                                    Space_Colors().color_map[self.grid[i_key][j_key]["type"]],
                                                                    (pos[0], pos[1], self.rect_size,self.rect_size))

            pygame.display.update()
        # handle the game loop here
        pass
