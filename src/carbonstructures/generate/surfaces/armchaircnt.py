# import numpy as np
from math import sin, cos, pi
from . import data
import copy

__all__ = ['ArmchairCNT']

# function to initiate an airchair CNT with size in xyz-coordinate
class ArmchairCNT(object):
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

    def __init__(self, length, diameter, CC=1.418): 
        """
        Creates a Carbon Nanotube (CNT) instance:
            generated sheet is a VALID structure (no partial hexagons)
            generated sheet has x- and y-lengths LESS THAN OR EQUAL TO xlen and ylen

        Preconditions: 
            length and diameter must be floats
        """
        # set CNT tube length, CC_bond length, radius, hexagonal tube length
        self.CC_bond = CC
        self.index = self.radmatch(diameter / 2)
        self.radius = data.radii[self.index]
        #self.radius = diameter / 2
        self.hex_length = (length - self.CC_bond * cos(pi / 6.0)) // (2 * self.CC_bond * cos(pi / 6.0))
        self.length = (2 * self.hex_length + 1) * self.CC_bond * cos(pi / 6.0)
        
    def radmatch(self, target):
        """
        Scans lists from data.py for the closest fitting radii to the target:
            in the (rare) case of two equally close-fitting radii, the smaller tube will be chosen
            scanning is linear (O(N)) for now - working on inputting binary search
        
        Preconditions:
            target must be a float
        """

        # calculate starting difference between radius and target
        diff = abs(data.radii[0] - target)
        # set index to be returned by this function (matching radius/angle by index)
        ind = 0
        # run through list of radii
        for index in range(len(data.radii)):
            # recalculate difference between list radius and target
            temp = abs(data.radii[index] - target)
            # replace difference and index if difference is smaller than before
            if temp < diff:
                diff = temp
                ind = index
        return ind
    
    def generate_coords(self):
        # take index of closest-fitting radius with radmatch
        # index = self.radmatch(self.radius)
        # radius = data.radii[index]
        # calculate useful values: tube length, half of tube length, number of edges, 
        # separation angle, angular shift
        half = (self.length / 2)
        edges = self.index + 3
        angle = data.angles[self.index]
        shift = ((2 * pi) / edges) - angle
        
        # generate first circle of coordinates
        c1ang = 0
        c1 = [["{:.6f}".format(self.radius * cos(c1ang)),"{:.6f}".format(self.radius * sin(c1ang))]]
        c1ind = 1
        while c1ind < 2 * edges:
            if c1ind % 2:
                c1ang += shift
            else:
                c1ang += angle
            c1.append(["{:.6f}".format(self.radius * cos(c1ang)),"{:.6f}".format(self.radius * sin(c1ang))])
            c1ind += 1
        
        # generate second circle of coordinates
        c2ang = pi / edges
        c2 = [["{:.6f}".format(self.radius * cos(c2ang)),"{:.6f}".format(self.radius * sin(c2ang))]]
        c2ind = 1
        while c2ind < 2 * edges:
            if c2ind % 2:
                c2ang += shift
            else:
                c2ang += angle
            c2.append(["{:.6f}".format(self.radius * cos(c2ang)),"{:.6f}".format(self.radius * sin(c2ang))])
            c2ind += 1
        
        # generate axis coordinates
        axis = []
        axis_coord = -half
        while axis_coord <= half + 1:
            axis.append("{:.6f}".format(axis_coord))
            axis_coord += self.CC_bond * cos(pi / 6.0)
        
        # attach coordinates
        coordinates = []
        for i in range(len(axis)):
            if i % 2: 
                temp = copy.deepcopy(c1)
            else:
                temp = copy.deepcopy(c2)
            for j in range(len(temp)):
                temp[j].append(axis[i])
            for k in temp:
                coordinates.append(tuple(k))
                
        return [coordinates, half]