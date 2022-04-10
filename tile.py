import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
import random
from point import Point
import copy as cp
import random
import math


# Class used for modeling numbered tiles as in 2048
class Tile:
    # Class attributes shared among all Tile objects
    # ---------------------------------------------------------------------------
    # the value of the boundary thickness (for the boxes around the tiles)
    boundary_thickness = 0.004
    # font family and size used for displaying the tile number
    font_family, font_size = "Arial", 14

    # Constructor that creates a tile with 2 as the number on it
    def __init__(self, position=Point(0, 0)):

        random_list = [2, 4, 8]
        x = random.choice(random_list)
        if x == 2:
            # set the number on the tile
            self.number = 2
            # set the colors of the tile
            self.background_color = Color(255, 255, 255)  # background (tile) color
            self.foreground_color = Color(0, 100, 200)  # foreground (number) color
            self.box_color = Color(0, 100, 200)  # box (boundary) color

        elif x == 4:
            # set the number on the tile
            self.number = 4
            # set the colors of the tile
            self.background_color = Color(255, 235, 205)  # background (tile) color
            self.foreground_color = Color(0, 100, 200)  # foreground (number) color
            self.box_color = Color(0, 100, 200) # box (boundary) color

        elif x == 8:

            self.number = 8
            self.background_color = Color(255, 222, 173)  # background (tile) color
            self.foreground_color = Color(0, 100, 200)  # foreground (number) color
            self.box_color = Color(0, 100, 200)


        self.position = Point(position.x, position.y)
        random_index = random.randint(0, len(random_list) - 1)
        random_value = random_list[random_index]

    def double(self):
        self.number *= 2

    def move(self, dx, dy):
        self.position.translate(dx, dy)

    # Method for drawing the tile
    def draw(self, position, length=1):
        # draw the tile as a filled square
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        # draw the bounding box around the tile as a square
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()  # reset the pen radius to its default value
        # draw the number on the tile
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))

    def can_be_moved(self, moving_position):
        grid_h, grid_w = 20, 12

        if (self.position.x + moving_position.x >= 12) or (self.position.x + moving_position.x < 0):
            return False
        if (self.position.y + moving_position.y >= 20) or (self.position.y + moving_position.y < 0):
            return False

        return True