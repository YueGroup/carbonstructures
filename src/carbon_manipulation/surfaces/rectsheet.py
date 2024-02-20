# import numpy as np
from math import sin, cos, pi

# function to initiate a graphene sheet with size in xy-coordinate
class RectangularSheet(object):
    """
    Functions for initializing, generating coordinates for, and functionalizing rectangular graphene sheets

    Defaults:
        x-axis: zigzag side
        y-axis: armchair side
        z-axis: plane (z=0)
    
    Instance attributes: 
        len1 [float]: total specified length in x-direction
        len2 [float]: total specified length in y-direction
        CC [float]: carbon-carbon bond length
        hex_x [int]: number of hexagons in the x-direction
        hex_y [int]: number of hexagons in the y-direction

    Attribute notes:
        specified length paramters are MAXIMUM lengths. Sheets cannot be generated for all x/y lengths; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    def __init__(self, x, y, CC=1.418):
        """
        Creates a RectangularSheet instance:
            generated sheet is a VALID structure (no partial hexagons)
            generated sheet has dimensional lengths LESS THAN OR EQUAL TO x and y

        Preconditions: 
            xlen, ylen are floats
        """
        # set CC bond length
        self.CC = CC

        # hexagon unit lengths
        xunit = 2.0 * self.CC * cos(pi / 6.0)
        yunit = (1.0 + sin(pi / 6.0)) * self.CC

        # calculate sheet dimensions in hexagonal units 
        self.xhex = (x - self.CC * cos(pi / 6.0)) // xunit
        self.yhex = (y - self.CC * sin(pi / 6.0)) // yunit
        
        # raise exception if specified parameters are too small
        if (self.xhex <= 0) or (self.yhex <= 0): 
            raise Exception("Sheet dimensions too small!")
        
        # length and width of sheet (no partial hexagons)
        self.xlen = self.xhex * xunit
        self.ylen = self.yhex * yunit + self.CC * sin(pi / 6.0)
        
    def generate_coords(self, z=0.0):
    # def generate_coords(self,z=0.0):
        """
        Returns an list of coordinates, in tuples (x,y), representing the rectangular graphene sheet

        Parameters: 
            z: z-coordinate of sheet (default 0.00)
        """
        #need to have the option to specify x and y (at bottom left corner) for sheets in piston code
        # is the starting x, y here from bottom left


        # columns: number of unique x-coordinates
        columns = 2 * self.xhex + 2
        # rows: number of unique y-coordinates
        rows = 2 * self.yhex + 2

        # generate list of x-coordinates
        xcoordlist = []
        # xcoord = -(self.CC * cos(pi / 6.0)) + x
        xcoord = -(self.CC * cos(pi / 6.0))
        xcount = 0
        while xcount < columns:
            # xcoordlist.append(float("{:.6f}".format(xcoord)))
            xcoordlist.append("{:.6f}".format(xcoord))
            xcoord += self.CC * cos(pi / 6.0)
            xcount += 1

        # generate list of y-coordinates
        ycoordlist = []
        # ycoord = y
        ycoord = 0
        ycount = 0
        while ycount < rows:
            # ycoordlist.append(float("{:.6f}".format(ycoord))) 
            ycoordlist.append("{:.6f}".format(ycoord))    
            if ycount % 2: 
                ycoord += self.CC
            else:
                ycoord += self.CC * sin(pi / 6.0)
            ycount += 1

        # generate coordinates
        coordinates = [[xcoordlist[ind1], ycoordlist[ind2]]
                for ind2 in range(len(ycoordlist))
                for ind1 in range(len(xcoordlist))
                if (((ind2 + 1) % 4 == 0 or ind2 % 4 == 0) and ind1 % 2) or 
                   (not ((ind2 + 1) % 4 == 0 or ind2 % 4 == 0) and not ind1 % 2)]

#        if self.yhex % 2: 
#            coordinates.remove([xcoordlist[-1], 0])
#            coordinates.remove([xcoordlist[-1], ycoordlist[-1]])
#        else: 
#            coordinates.remove([xcoordlist[-1], 0])
#            coordinates.remove([0, ycoordlist[-1]])

        for index in range(len(coordinates)):
            coordinates[index].append("{:.6f}".format(z))
            # coordinates[index].append("{:.6f}".format(z))
            coordinates[index] = tuple(coordinates[index])
        
        return [coordinates, xcoordlist[0], xcoordlist[-1], ycoordlist[0], ycoordlist[-1]]

