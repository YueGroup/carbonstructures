# import numpy as np
from math import sin, cos, pi

# function to initiate a graphene sheet with size in xy-coordinate
class RectangularSheet(object):
    """
    Functions for initializing, generating coordinates for, and functionalizing rectangular graphene sheets

    Notation notes: 
        x-direction is zigzag side
        y-direction is airmchair side
        all lengths are in Angstroms
    
    Instance attributes: 
        xlen [float]: total specified length in x-direction
        ylen [float]: total specified length in y-direction
        CC_bond [float]: carbon-carbon boind length
        hex_x [int]: number of hexagons in the x-direction
        hex_y [int]: number of hexagons in the y-direction

    Attribute notes:
        specified length paramters are MAXIMUM lengths. Sheets cannot be generated for all x/y lengths; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    def __init__(self, xlen, ylen):
        """
        Creates a RectangularSheet instance:
            generated sheet is a VALID structure (no partial hexagons)
            generated sheet has x- and y-lengths LESS THAN OR EQUAL TO xlen and ylen

        Preconditions: 
            xlen, ylen are floats
        """
        # set xlen, ylen, CC_bond variables
        self.xlen = xlen
        self.ylen = ylen
        self.CC_bond = 1.41

        # hexagon unit lengths
        unit_x = 2.0 * self.CC_bond * cos(pi / 6.0)
        unit_y = (1.0 + sin(pi / 6.0)) * self.CC_bond

        # calculate sheet dimensions in hexagonal units
        self.hex_x = (xlen - self.CC_bond * cos(pi / 6.0)) // unit_x
        self.hex_y = (ylen - self.CC_bond * sin(pi / 6.0)) // unit_y

        if (self.hex_x <= 0) or (self.hex_y <= 0): 
            raise Exception("Dimensions too small")

        carbons_per_row = 1 + self.hex_x * 2
        self.n_Cs = carbons_per_row * (self.hex_y + 1)
        
    def generate_coords(self, x=0.0, y=0.0):
        """
        Returns an list of coordinates, in tuples (x,y), representing the rectangular graphene sheet

        Parameters: 
            x: bottom left corner x-coordinate (default 0.00)
            y: bottom left corner y-coordinate (default 0.00)
        """
        # columns: number of unique x-coordinates
        columns = 2 * self.hex_x + 2
        # rows: number of unique y-coordinates
        rows = 2 * self.hex_y + 2

        # generate list of x-coordinates
        x_coordinates = [x]
        x_counter = 1
        while x_counter < columns:
            x += self.CC_bond * cos(pi / 6.0)
            x_coordinates.append(x)
            x_counter += 1

        # generate list of y-coordinates
        y_coordinates = [y]
        y_counter = 1
        while y_counter < rows:
            if y_counter % 2: 
                y += self.CC_bond * sin(pi / 6.0)
            else:
                y += self.CC_bond
            y_coordinates.append(y)
            y_counter += 1

        # generate coordinates
        
        print(x_coordinates)
        print(y_coordinates)

        coordinates = [(x_coordinates[x_ind], y_coordinates[y_ind])
                for y_ind in range(len(y_coordinates))
                for x_ind in range(len(x_coordinates))
                if (((y_ind + 1) % 4 == 0 or y_ind % 4 == 0) and x_ind % 2) or 
                   (not ((y_ind + 1) % 4 == 0 or y_ind % 4 == 0) and not x_ind % 2)]
    
        # remove excess coordinates
        
        if self.hex_y % 2: 
            coordinates.remove((x_coordinates[-1], 0))
            coordinates.remove((x_coordinates[-1], y_coordinates[-1]))
        else: 
            coordinates.remove((x_coordinates[-1], 0))
            coordinates.remove((0, y_coordinates[-1]))
        print(len(coordinates))
        return coordinates   
        
        # make list of columns/rows, form relevant tuples into a masterlist
        