# import numpy as np
from math import sin, cos, pi, asin
import data

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

    def __init__(self, length, diameter, form="zigzag"): 
        """
        Creates a Carbon Nanotube (CNT) instance:
            generated sheet is a VALID structure (no partial hexagons)
            generated sheet has x- and y-lengths LESS THAN OR EQUAL TO xlen and ylen

        Preconditions:  
            form must be zigzag (default), armchair, or chiral (to be added later)
            length and diameter must be floats
        """
        self.form = form
        self.length = length
        self.CC_bond = 1.41
        if form == "zigzag":
            self.ring_atoms = pi // asin((2 * self.CC_bond * cos(pi / 6.0)) / diameter)
            self.hex_length = (length - self.CC_bond * sin(pi / 6.0)) // ((1.0 + sin(pi / 6.0)) * self.CC_bond)
            self.radius = (self.CC_bond * cos(pi / 6.0)) / sin(pi / self.ring_atoms)
        elif form == "armchair":
            self.radius = diameter / 2
            self.hex_length = (length - self.CC_bond * cos(pi / 6.0)) // (2 * self.CC_bond * cos(pi / 6.0))
        elif form == "chiral":
            return "unfinished"
        else: 
            raise Exception("Invalid form")
        
    def radmatch(self, target):
        #two lists, radius, inner angle
        return 2
    
    def generate_coords_armchair(self, x=0.0, y=0.0, z=0.0, int_ang=0.0):
        # takes index from 
        index = self.radmatch(self.radius)
        atom_length = 2 * self.hexlength + 2
        edges = index + 3
        angle = data.angles[index]
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
        
        # generate z coordinates
        z = []
        z_ind = 0
        while z_ind < atom_length:
            z.append([z_ind * self.CC_bond * cos(pi / 6)])
            z_ind += 1
        
        # attach coordinates
        coordinates = []
        for i in range(len(z)):
            if i % 2: 
                temp = c1
            else:
                temp = c2
            print(temp)
            for j in range(len(temp)):
                coordinates.append(tuple(temp[j] + z[i]))
                # note, to add instead x/y, modify where it is being added to the list
             
        return coordinates