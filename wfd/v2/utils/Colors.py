"""handles the colors and their mappings"""



class Color:
    def __init__(self):
        pallete = {
        "Timberwolf":(218, 221, 216),
        "Jet":(51, 50, 50),
        "Russian Green":(90, 147, 103),
        "Brown Sugar":(181, 107, 69),
        "Metallic Seaweed":(8, 127, 140)}

        self.background = pallete["Jet"]
        self.button = pallete["Metallic Seaweed"]
        self.white = (255,255,255)
        self.black = (0,0,0)
