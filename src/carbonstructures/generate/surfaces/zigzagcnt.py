# WORK IN PROGRESS

# import numpy as np
from math import sin, cos, pi, asin, floor
import copy

__all__ = ['ZigzagCNT']
# function to initiate a zigzag CNT with size in xyz-coordinate
class ZigzagCNT(object):
    """
    Functions for initializing, generating coordinates for, and functionalizing zigzag CNTs

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
            generated CNT is a VALID structure (no partial hexagons)
            generated CNT has length LESS THAN OR EQUAL TO input length

        Preconditions:  
            form must be zigzag (default), armchair, or chiral (to be added later)
            length and diameter must be floats
        """
        self.CC_bond = CC
        
        # humber of carbon atoms on one ring
        self.ring_atoms = pi // asin((2 * self.CC_bond * cos(pi / 6.0)) / diameter)

        # number of hexagons spanning the length
        self.hex_length = (length - self.CC_bond * sin(pi / 6.0)) // (self.CC_bond * (1 + sin(pi / 6.0)))

        # radius of CNT (less than or equal input diameter/2)
        self.radius = (self.CC_bond * cos(pi / 6.0)) / sin(pi / self.ring_atoms)

        # length of zigzag CNT (no partial hexagon)
        self.length = self.CC_bond * (self.hex_length * (1 + sin(pi / 6.0)) + sin(pi / 6.0))
        
    # def axial_circle(self, z=0.0, axis="aligned"):
    #     """
    #     Returns an list of coordinates, in [x,y,z], representing the axial circle at a given z
    #     Center of circle will be at (0.0, 0.0, z)

    #     Parameters: 
    #         z [float]: fixed z coords for all points in axial circle
    #         axis = aligned or shifted from x-y
    #     """
    #     # radius of cylinder
    #     rad = self.radius
    #     # angle between two adjacent Carbon atoms in circle
    #     angular = (2 * pi) / self.ring_atoms
    #     # generate x, y coords for atoms on circle
    #     coords = []
    #     if axis == "aligned":
    #         shift = 0
    #     else:
    #         shift = angular/2
    
    #     angle = 0
    #     while angle+shift < 2*pi+shift:
    #         x = rad*cos(angle)
    #         y = rad*sin(angle) 
    #         coords.append([x,y,z])
    #         angle += angular
    #     return coords    

    # def generate_coords(self, x=0.0, y=0.0, z=0.0):
    #     """
    #     Returns an list of coordinates, in [x,y,z], representing the zigzag cnt

    #     Parameters: 
    #         x, y [float]:  at axial center of CNT
    #         z [float]: at center of CNT's left-most end 
    #     """

    #     # generate coords for CNT with one unit hexagon in length at a time
    #     coords =[]
    #     z1 = z #outmost z-coord
    #     # highest possible z-coord for axial circle
    #     max_z = self.length - 2*self.CC_bond - z
    #     while z1 <= max_z:
    #         top = self.axial_circle(z=z1,axis="aligned")
    #         bot = self.axial_circle(z=z1+2*self.CC_bond,axis="aligned")
    #         side1 = self.axial_circle(z=z1+0.5*self.CC_bond,axis="shifted")
    #         side2 = self.axial_circle(z=z1+1.5*self.CC_bond,axis="shifted")
    #         coords += top+side1+side2+bot
    #         z1 += 3*self.CC_bond
    #     a = coords[0][1]
    #     print (type(a))
    #     print (a)
    #     print (a)
    #     return coords
    
    def generate_coords(self):
        half = (self.length / 2)
        edges = self.ring_atoms
        shift = ((2 * pi) / edges)
        
        # generate first circle of coordinates
        c1ang = 0
        c1 = [["{:.6f}".format(self.radius * cos(c1ang)),"{:.6f}".format(self.radius * sin(c1ang))]]
        c1ind = 1
        while c1ind < edges:
            c1ang += shift
            c1.append(["{:.6f}".format(self.radius * cos(c1ang)),"{:.6f}".format(self.radius * sin(c1ang))])
            c1ind += 1
        
        # generate second circle of coordinates
        c2ang = pi / edges
        c2 = [["{:.6f}".format(self.radius * cos(c2ang)),"{:.6f}".format(self.radius * sin(c2ang))]]
        c2ind = 1
        while c2ind < edges:
            c2ang += shift
            c2.append(["{:.6f}".format(self.radius * cos(c2ang)),"{:.6f}".format(self.radius * sin(c2ang))])
            c2ind += 1
        
        # generate axis coordinates
        axis = []
        axis_coord = -half
        axis_ind = 0
        while axis_coord <= half + 1:
            axis.append("{:.6f}".format(axis_coord))
            if axis_ind % 2:
                axis_coord += self.CC_bond
            else: 
                axis_coord += self.CC_bond * sin(pi / 6.0)
            axis_ind +=1
        
        print(axis)
        
        # attach coordinates
        coordinates = []
        for i in range(len(axis)):
            if i % 4 == 1 or i % 4 == 2: 
                temp = copy.deepcopy(c1)
            else:
                temp = copy.deepcopy(c2)
            for j in range(len(temp)):
                temp[j].append(axis[i])
            for k in temp:
                coordinates.append(tuple(k))

             
        return [coordinates, half]     