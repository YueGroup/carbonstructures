# import numpy as np
from math import sin, cos, pi
import networkx as nx

__all__ = ['RectangularSheet']

# function to initiate a graphene sheet with size in xy-coordinate
class RectangularSheet(object):
    """
    Object class for a rectangular graphene sheet

    Defaults:
        x-axis: zigzag side
        y-axis: armchair side
        z-axis: plane (z=0)
    
    Instance attributes: 
        CC [float]: carbon-carbon bond length (Angstroms)
        xlen [float]: actual length (in the x-direction) (Angstroms)
        ylen [float]: actual width (in the y-direction) (Angstroms)

    Attribute notes:
        Specified length paramters are MAXIMUM lengths. Sheets cannot be generated for all x,y lengths; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    # object initialization
    def __init__(self, x, y, CC):
        # Initialize CC bond length
        self.CC = CC

        # Calculate hexagonal unit lengths
        xunit = 2.0 * self.CC * cos(pi / 6.0)
        yunit = (1.0 + sin(pi / 6.0)) * self.CC

        # Calculate sheet dimensions in terms of hexagonal units 
        self.xhex = (x - self.CC * cos(pi / 6.0)) // xunit
        self.yhex = (y - self.CC * sin(pi / 6.0)) // yunit
        # Corrects y-hexagon count to be an odd number
        if self.yhex % 2 == 0:
            self.yhex -= 1
        # Raise exception if the specified sheet dimensions are too small
        if (self.xhex <= 0) or (self.yhex <= 0): 
            raise Exception("Sheet dimensions too small!")
        # Calculates length and width of sheet (no partial hexagons)
        self.xlen = self.xhex * xunit
        self.ylen = self.yhex * yunit + self.CC * sin(pi / 6.0)
    
    # Generate coordinates (list of tuples form)
    def generate_coords(self, z=0.0):
        # columns: number of unique x-coordinates
        # rows: number of unique y-coordinates
        columns = 2 * self.xhex + 2
        rows = 2 * self.yhex + 2

        # Generate list of x-coordinates, starting at x = 0
        xcoordlist = []
        xcoord = 0
        xcount = 0
        while xcount < columns:
            # Formats x-coordinates to 6 decimal places
            xcoordlist.append("{:.6f}".format(xcoord))
            xcoord += self.CC * cos(pi / 6.0)
            xcount += 1

        # Generate list of y-coordinates, starting at y = 0
        ycoordlist = []
        ycoord = 0
        ycount = 0
        while ycount < rows:
            # Formats y-coordinates to 6 decimal places
            ycoordlist.append("{:.6f}".format(ycoord))
            # Alternates value added to y-coordinates
            if ycount % 2: 
                ycoord += self.CC
            else:
                ycoord += self.CC * sin(pi / 6.0)
            ycount += 1

        # Generate list of [x,y] coordinate lists
        coordinates = [[xcoordlist[ind1], ycoordlist[ind2]]
                for ind2 in range(len(ycoordlist))
                for ind1 in range(len(xcoordlist))
                if (((ind2 + 1) % 4 == 0 or ind2 % 4 == 0) and ind1 % 2) or 
                   (not ((ind2 + 1) % 4 == 0 or ind2 % 4 == 0) and not ind1 % 2)]

        # Append z-coordinates and convert coordinate lists to tuples
        for index in range(len(coordinates)):
            # Formats z-coordinates to 6 decimal places
            coordinates[index].append("{:.6f}".format(z))
            coordinates[index] = tuple(coordinates[index])
        
        return coordinates
        # return [coordinates, xcoordlist[0], xcoordlist[-1], ycoordlist[0], ycoordlist[-1]]

    # Generates coordinates (graph form)
    def carbon_graph(self, z=0.0):
        coordinates = self.generate_coords(z)
        graph = nx.Graph()
        
        # Add a node for each atom
        # Stored data: index (numerical starting from 0), position (tuple coordinates), atom type (atomic symbol and assignment in LAMMPS)
        for index, carbon_coord in enumerate(coordinates):
            graph.add_node(index, pos=carbon_coord, type=['C','1'])

        # Add edges between all atoms within a C-C bond length of each other (including buffer space)
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                if sum((float(coordinates[i][k]) - float(coordinates[j][k]))**2 for k in range(len(coordinates[i])))**0.5 <= (self.CC + 0.01):
                    graph.add_edge(i, j)
        
        return graph