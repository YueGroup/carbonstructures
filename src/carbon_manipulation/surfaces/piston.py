# parameters: sheet dimensions, tube diameter
# generate sheet, tube based on parameters. center will be the center of the tube
# make hole in one sheet by taking out a circle. measure the circle (either a central atom or the center of a hexagon)

# dimensions in terms of hexagons
# 


# input parameters: 
# 

# steps
# generate cnt
from math import sin,cos,pi
import armchaircnt
import zigzagcnt
import rectsheet


class Piston(object):
    """
    Functions for initializing, generating coordinates for, and functionalizing zigzag piston made of 
    two same-sized graphene sheets and one CNT, origin will be at center of CNT

    Notation notes: 
        the form parameter indicates the direction in which the carbon nanotube has been rolled. "armchair/zigzag" indicate the type
        of edge parallel to the rolled edge; "chiral" indicates any tubes rolled an an angle
    
    Instance attributes: 
        form [str]: form of the nanotube (zigzag, airmchair, chiral) 
        cntlength [float]: total length of the tube specified
        xlen [float]: total specified length in x-direction for graphene sheet
        ylen [float]: total specified length in y-direction for graphene sheet
        CC_bond [float]: carbon-carbon bond length
        radius [float]: radius of the tube (rounded down to best radius from input)

    Attribute notes:
        specified length parameters are MAXIMUM lengths. Sheets/CNTs cannot be generated for all lengths/diameters; the generation will
        provide the closest estimate that is smaller than the specified parameters
    """
    def __init__(self,form,cntlenght, diameter, xlen, ylen):
        if not form == "zigzag" or "armchair" or "chiral":
            raise Exception("There is no such form of CNT")
        self.form = form
        if form == "zigzag":
            self.cnt = zigzagcnt.ZigCNT(cntlenght,diameter)
        elif form == "armchair":
            self.cnt = armchaircnt.ArmCNT(cntlenght,diameter)
        elif form == "chiral":
            self.cnt = "unfinished"
        self.sheetL = rectsheet.RectangularSheet(xlen,ylen)
        self.sheetR = rectsheet.RectangularSheet(xlen,ylen)

    def generate_coords_piston(self, x=0.0, y=0.0, z=0.0, dist_left=0.0, dist_right=0.0):
        """
        Returns an list of coordinates, in [x,y,z], representing the piston

        Parameters: 
            x, y, z [float]: axial center of CNT
            dist_left [float]: distance of left graphene sheet from the end of CNT
            dist_right [float]: distance of right graphene sheet from the end of CNT
        """
        # generate CNT coordinates
        if self.form == "zigzag":
            coord_cnt = self.cnt.generate_coords_zigzag(x,y,z)
        # elif self == "chiral":
        #     coord_cnt = self.cnt.generate_coords_armchair()

        # z-coords for left and right graphene sheet
        zL = (z-self.cnt.length*0.5) - dist_left
        zR = (z+self.cnt.length*0.5) + dist_right

        # coordinate of bottom-left C atom in graphene sheet
        x_bot = x-self.sheetL.xlen
        y_bot = y-self.sheetL.ylen

        # generate left and right graphene sheet coordinate
        coord_sheetL = self.sheetL.generate_coords(x_bot,y_bot,zL)
        coord_sheetR = self.sheetR.generate_coords(x_bot,y_bot,zR)

        coords = coord_sheetL + coord_cnt + coord_sheetR
        return coords