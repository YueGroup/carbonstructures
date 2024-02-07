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
        len1 [float]: total specified length in x-direction
        len2 [float]: total specified length in y-direction
        CC_bond [float]: carbon-carbon bond length
        hex_x [int]: number of hexagons in the x-direction
        hex_y [int]: number of hexagons in the y-direction

    Attribute notes:
        specified length paramters are MAXIMUM lengths. Sheets cannot be generated for all x/y lengths; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    def __init__(self, one, two, plane):
        """
        Creates a RectangularSheet instance:
            generated sheet is a VALID structure (no partial hexagons)
            generated sheet has dimensional lengths LESS THAN OR EQUAL TO len1 and len2

        Preconditions: 
            one, two are floats
            plane is 0, 1, or 2
                0: x = a, y = len1, z = len2
                1: x = len1, y = a, z = len2
                2: x = len1, y = len2, z = a
        """
        # set CC bond length
        self.CC_bond = 1.41
        
        # set plane (0: x = 0, 1: y = 0, 2: z = 0)
        self.plane = plane
        # check that the plane is valid
        if plane not in [0, 1, 2]:
            raise Exception("Not a valid plane for the surface!")

        # hexagon unit lengths
        unit_1 = 2.0 * self.CC_bond * cos(pi / 6.0)
        unit_2 = (1.0 + sin(pi / 6.0)) * self.CC_bond

        # calculate sheet dimensions in hexagonal units
        self.hex_1 = (one - self.CC_bond * cos(pi / 6.0)) // unit_1
        self.hex_2 = (two - self.CC_bond * sin(pi / 6.0)) // unit_2 
        
        # raise exception if specified parameters are too small
        if (self.hex_1 <= 0) or (self.hex_2 <= 0): 
            raise Exception("Dimensions too small!")
        
        # length and width of sheet (no partial hexagons)
        self.len1 = self.hex_1 * unit_1 + self.CC_bond * cos(pi / 6.0)
        self.len2 = self.hex_2 * unit_2 + self.CC_bond * sin(pi / 6.0)
        
    def generate_coords(self, one=0.0, two=0.0, three=0.0):
        """
        Returns an list of coordinates, in tuples (x,y), representing the rectangular graphene sheet

        Parameters: 
            x: bottom left corner x-coordinate (default 0.00)
            y: bottom left corner y-coordinate (default 0.00)
            z: z-coordinate of sheet (default 0.00)
        """
        # columns: number of unique x-coordinates
        columns = 2 * self.hex_1 + 2
        # rows: number of unique y-coordinates
        rows = 2 * self.hex_2 + 2

        # generate list of x-coordinates
        coordinates1 = [one]
        counter1 = 1
        while counter1 < columns:
            one += self.CC_bond * cos(pi / 6.0)
            coordinates1.append(one)
            counter1 += 1

        # generate list of y-coordinates
        coordinates2 = [two]
        counter2 = 1
        while counter2 < rows:
            if counter2 % 2: 
                two += self.CC_bond * sin(pi / 6.0)
            else:
                two += self.CC_bond
            coordinates2.append(two)
            counter2 += 1

        # generate coordinates
        coordinates = [[coordinates1[ind1], coordinates2[ind2]]
                for ind2 in range(len(coordinates2))
                for ind1 in range(len(coordinates1))
                if (((ind2 + 1) % 4 == 0 or ind2 % 4 == 0) and ind1 % 2) or 
                   (not ((ind2 + 1) % 4 == 0 or ind2 % 4 == 0) and not ind1 % 2)]

        if self.hex_2 % 2: 
            coordinates.remove([coordinates1[-1], 0])
            coordinates.remove([coordinates1[-1], coordinates2[-1]])
        else: 
            coordinates.remove([coordinates1[-1], 0])
            coordinates.remove([0, coordinates2[-1]])

        for index in range(len(coordinates)):
            coordinates[index].insert(self.plane, three)
            coordinates[index] = tuple(coordinates[index])
        
        return coordinates