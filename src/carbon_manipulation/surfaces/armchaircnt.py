# import numpy as np
from math import sin, cos, pi, asin
from data import radii, angles
import copy

# function to initiate a graphene sheet with size in xy-coordinate
class CNT(object):
    """
    Functions for initializing, generating coordinates for, and functionalizing rectangular graphene sheets

    Notation notes: 
        the form parameter indicates the direction in which the carbon nanotube has been rolled. "armchair/zigzag" indicate the type
        of edge parallel to the rolled edge; "chiral" indicates any tubes rolled an an angle
    
    Instance attributes: 
        form [str]: form of the nanotube (zigzag, airmchair, chiral) 
        length [float]: total length of the tube specified
        CC_bond [float]: carbon-carbon bond length
        hex_length [float]: total length of the tube specified, in terms of hexagons
        ring_atoms [float]: total number of atoms that comprise one circular layer of the sheet (float, but whole number)
        diameter [float]: diameter of the tube (rounded down to best diameter from input)

    Attribute notes:
        specified length parameters are MAXIMUM lengths. Sheets cannot be generated for all lengths/diameters; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """

    def __init__(self, length, diameter): 
        """
        Creates a Carbon Nanotube (CNT) instance:
            generated sheet is a VALID structure (no partial hexagons)
            generated sheet has x- and y-lengths LESS THAN OR EQUAL TO xlen and ylen

        Preconditions:  
            form must be zigzag (default), armchair, or chiral (to be added later)
            length and diameter must be floats
        """
        self.length = length
        self.CC_bond = 1.41
        self.radius = diameter / 2
        self.hex_length = (length - self.CC_bond * cos(pi / 6.0)) // (2 * self.CC_bond * cos(pi / 6.0))
        
    def radmatch(self, target):
        # linear scan through radii list to match the index of the closest-fitting radius. The smaller value
        # wins out in the case of a tie. 
        # working on replacing with binary search/match
        diff = abs(radii[0] - target)
        ind = 0
        for index in range(len(radii)):
            temp = abs(radii[index] - target)
            if temp < diff:
                diff = temp
                ind = index
        return ind
    
    def generate_coords_armchair(self, axis_index = 0, int_ang=0.0):
        # takes index from 
        index = self.radmatch(self.radius)
        tube_length = (2 * self.hexlength + 1) * self.CC_bond * cos(pi / 6.0)
        half = (tube_length / 2)
        edges = index + 3
        angle = angles[index]
        shift = ((2 * pi) / edges) - angle
        
        # generate first circle of coordinates
        c1ang = int_ang
        c1 = [[self.radius * cos(c1ang),self.radius * sin(c1ang)]]
        c1ind = 1
        while c1ind < 2 * edges:
            if c1ind % 2:
                c1ang += shift
            else:
                c1ang += angle
            c1.append([self.radius * cos(c1ang),self.radius * sin(c1ang)])
            c1ind += 1
        
        # generate second circle of coordinates
        c2ang = int_ang + pi / edges
        c2 = [[self.radius * cos(c2ang),self.radius * sin(c2ang)]]
        c2ind = 1
        while c2ind < 2 * edges:
            if c2ind % 2:
                c2ang += shift
            else:
                c2ang += angle
            c2.append([self.radius * cos(c2ang),self.radius * sin(c2ang)])
            c2ind += 1
        
        # generate axis coordinates
        axis = []
        axis_coord = -half
        while axis_coord <= half + 1:
            axis.append([axis_coord])
            axis_coord += self.CC_bond * cos(pi / 6.0)
        
        # attach coordinates
        coordinates = []
        for i in range(len(axis)):
            if i % 2: 
                temp = copy.deepcopy(c1)
            else:
                temp = copy.deepcopy(c2)
            print(temp)
            for j in range(len(temp)):
                temp[j].insert(axis_index, axis[i])
            for k in temp:
                coordinates.append(tuple(k))
                # note, to add instead x/y, modify where it is being added to the list
             
        return coordinates