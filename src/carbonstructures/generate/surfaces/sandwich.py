# import numpy as np
from math import sin, cos, pi
from . import sheet
import networkx as nx

__all__ = ['Sandwich']

# function to initiate a graphene sheet with size in xy-coordinate
class Sandwich(object):
    """
    Object class for a 'graphene sandwich' configuration

    Defaults:
        x-axis: zigzag side
        y-axis: armchair side
        z-axis: plane (z=0)
    
    Instance attributes: 
        gap [float]: gap size between the sheets (Angstroms)
        CC [float]: carbon-carbon bond length (Angstroms)
        sheet [RectangularSheet object]: generated sheet based on given length and width directions

    Attribute notes:
        Specified length paramters are MAXIMUM lengths. Sheets cannot be generated for all x,y lengths; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    def __init__(self, x, y, g, CC):
        self.gap = g
        self.CC = CC
        self.sheet = sheet.RectangularSheet(x,y,CC)
    
    # Generate coordinates (list of tuples form)
    def generate_coords(self):
        sheet1 = self.sheet.generate_coords()
        sheet2 = self.sheet.generate_coords(self.gap)
        coordinates = sheet1 + sheet2

        return coordinates

    # Generate coordinates (graph form)
    def carbon_graph(self):
        coordinates = self.generate_coords()
        graph = nx.Graph()
        
        # Add a node for each atom
        # Stored data: index (numerical starting from 1), position (tuple coordinates), atom type (atomic symbol and assignment in LAMMPS)
        for index, carbon_coord in enumerate(coordinates):
            graph.add_node(index, pos=carbon_coord, type=['C','1'])

        # Add edges between all atoms within a C-C bond length of each other (including buffer space)
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                if sum((float(coordinates[i][k]) - float(coordinates[j][k]))**2 for k in range(len(coordinates[i])))**0.5 <= (self.CC + 0.01):
                    graph.add_edge(i, j)
        
        return graph