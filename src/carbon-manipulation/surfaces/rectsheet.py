import numpy as np
from math import sin, cos, pi

# function to initiate a graphene sheet with size in xy-coordinate
class RectangularSheet(object)
    def __init__(self, xlen, ylen):
        # zigzag side is x side
        # armchair side is y side
        # length in Angstroms
        self.CC = 1.41
        # len represents full length/width of sheet
        self.xlen = xlen
        self.ylen = ylen
        # unit lengths used to calculate sheet dimensions hexagons
        unit_x = 2.0 * self.CC * cos(pi / 6.0)
        unit_y = 1.5 * self.CC
        # calculate sheet dimensions in hexagons
        self.hex_x = xlen // unit_x
        self.hex_y = (ylen - 0.5 * self.CC) // unit_y

        if not self.hex_y % 2:
            self.hex_y -= 1

        if (self.hex_x <= 0) or (self.hex_y <= 0): 
            raise Exception("Dimensions too small")