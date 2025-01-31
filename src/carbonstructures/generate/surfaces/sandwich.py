# import numpy as np
from math import sin, cos, pi
from . import sheet
import networkx as nx

__all__ = ['Sandwich']

# function to initiate a graphene sheet with size in xy-coordinate
class Sandwich(object):
    """
    Functions for initializing graphene sandwiches

    Defaults:
        x-axis: zigzag side
        y-axis: armchair side
        z-axis: plane (z=0)

    Attribute notes:
        specified length parameters are MAXIMUM lengths. Sheets cannot be generated for all x/y lengths; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    def __init__(self, x, y, g, CC=1.418):
        self.gap = g
        self.CC = CC
        self.sheet = sheet.RectangularSheet(x,y,CC)
        
    def generate_coords(self):
        sheet1 = self.sheet.generate_coords()[0]
        sheet2 = self.sheet.generate_coords(self.gap)[0]
        coordinates = sheet1 + sheet2

        return coordinates

    def carbon_graph(self):
        coordinates = self.generate_coords()
        graph = nx.Graph()
        
        # Add a node with position attribute for each carbon
        for index, carbon in enumerate(coordinates):
            graph.add_node(index, pos=carbon, type=['C','1'])

        # Add edges based on the bond length
        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                if sum((float(coordinates[i][k]) - float(coordinates[j][k]))**2 for k in range(len(coordinates[i])))**0.5 <= (self.CC + 0.01):
                    graph.add_edge(i, j)
        
        return graph