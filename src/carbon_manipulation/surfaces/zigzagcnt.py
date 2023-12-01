# import numpy as np
from math import sin, cos, pi, asin, floor

# function to initiate a CNT with size in xyz-coordinate
class ZigCNT(object):
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

    def __init__(self, length, diameter): 
        """
        Creates a Carbon Nanotube (CNT) instance:
            generated CNT is a VALID structure (no partial hexagons)
            generated CNT has length LESS THAN OR EQUAL TO input length

        Preconditions:  
            form must be zigzag (default), armchair, or chiral (to be added later)
            length and diameter must be floats
        """
        self.CC_bond = 1.41
        
        # humber of carbon atoms on one ring
        self.ring_atoms = pi // asin((2 * self.CC_bond * cos(pi / 6.0)) / diameter)

        # number of hexagons spanning the length
        self.hex_length = floor(4/3*length-2/3)

        # radius of CNT (less than or equal input diameter/2)
        self.radius = (self.CC_bond * cos(pi / 6.0)) / sin(pi / self.ring_atoms)

        # length of zigzag CNT (no partial hexagon)
        self.length = self.hex_length*2*self.CC_bond - (self.hex_length-1)*0.5*self.CC_bond

        #if form == "zigzag":
        # self.hex_length = (length - self.CC_bond * sin(pi / 6.0)) // ((1.0 + sin(pi / 6.0)) * self.CC_bond)
        # elif form == "armchair":
        #     return "unfinished"
        # elif form == "chiral":
        #     return "unfinished"
        # else: 
        #     raise Exception("Invalid form")
        
    def axial_circle(self, z=0.0, axis="aligned"):
        """
        Returns an list of coordinates, in [x,y,z], representing the axial circle at a given z
        Center of circle will be at (0.0, 0.0, z)

        Parameters: 
            z [float]: fixed z coords for all points in axial circle
            axis = aligned or shifted from x-y
        """
        # radius of cylinder
        rad = self.radius
        # angle between two adjacent Carbon atoms in circle
        angular = (2 * pi) / self.ring_atoms
        # generate x, y coords for atoms on circle
        coords = []
        if axis == "aligned":
            shift = 0
        else:
            shift = angular/2
    
        angle = 0
        while angle+shift < 2*pi+shift:
            x = rad*cos(angle)
            y = rad*sin(angle) 
            coords.append([x,y,z])
            angle += angular
        return coords    

    def generate_coords_zigzag(self, x=0.0, y=0.0, z=0.0):
        """
        Returns an list of coordinates, in [x,y,z], representing the zigzag cnt

        Parameters: 
            x, y, z [float]: axial center of CNT, grows out in symmetrical left and right z direction
        """

        # generate coords for CNT with one unit hexagon in length at a time
        coords =[]
        z1 = z #outmost z-coord
        # highest possible z-coord for axial circle
        max_z = self.length - 2*self.CC_bond - z
        while z1 <= max_z:
            top = self.axial_circle(z=z1,axis="aligned")
            bot = self.axial_circle(z=z1+2*self.CC_bond,axis="aligned")
            side1 = self.axial_circle(z=z1+0.5*self.CC_bond,axis="shifted")
            side2 = self.axial_circle(z=z1+1.5*self.CC_bond,axis="shifted")
            coords += top+side1+side2+bot
            z1 += 3*self.CC_bond
        return coords



        # # define atom_length to be the number of atoms in the positive x direction
        # atom_length = 2 * self.hex_length + 2

        # # define angular to be the angle between two atoms of equal radius
        # angular = (2 * pi) / self.ring_atoms

        # define points on a circle for the non-axial atom coordinates


        
        # # define points on a circle for the non-axial atom coordinates
        # circ1anglesum = 0
        # circ1angles = [circ1anglesum]
        # while circ1anglesum < 2 * pi:
        #     circ1anglesum += angular
        #     circ1angles.append(circ1anglesum)

        # circ2anglesum = angular / 2
        # circ2angles = [circ2anglesum]
        # while circ2anglesum < 2 * pi + angular / 2:
        #     circ2anglesum += angular
        #     circ2angles.append(circ2anglesum)
        
        # x_coordinates = [x]
        # x_counter = 1
        # while x_counter < atom_length:
        #     x += self.CC_bond * cos(pi / 6.0)
        #     x_coordinates.append(x)
        #     x_counter += 1


        
        # coordinates = []
        
        
        
        
         
        
        
        # make list of columns/rows, form relevant tuples into a masterlist
        