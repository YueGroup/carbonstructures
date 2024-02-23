from math import sin,cos,pi,sqrt
from carbon_manipulation.surfaces import armchaircnt,zigzagcnt,rectsheet

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
    def __init__(self, xlen, ylen, cntlength, diameter, cntform = "arm", CC=1.418):
        self.form = cntform
        if cntform not in ["zig", "arm", "chiral"]:
            raise Exception("There is no such form of CNT")
        if cntform == "zig":
            self.cnt = zigzagcnt.ZigzagCNT(cntlength,diameter,CC)
        elif cntform == "arm":
            self.cnt = armchaircnt.ArmchairCNT(cntlength,diameter,CC)
        elif cntform == "chiral":
            pass
            # self.cnt = "unfinished"
        self.sheet = rectsheet.RectangularSheet(xlen,ylen)
    
    def poke(self, coordinates, delta=0.0):
        """
        Helper function to remove center atoms on graphene sheets that lay beyond the radius of cnt

        Parameters:
            coordinates [list]: list of tuples that contains xyz corrdinates of graphene sheet
            delta [float]: wiggle room to cut out atoms less than or equal to delta-Angstrom close to CNT
        Return:
            list of tuples containing corrdinates of poke graphene sheet
        """
        # coordinates is a list of atom coordinates in the graphene sheet. 
        
        # identify center of sheet
        centerx = (float(coordinates[1]) + float(coordinates[2])) / 2
        centery = (float(coordinates[3]) + float(coordinates[4])) / 2
        coords = coordinates[0]
        
        for index in range(len(coords)):
            # convert from tuple to list
            coords[index] = list(coords[index])
        
        new_coords = []
        for coord in coords:
            if sqrt((float(coord[0]) - centerx) ** 2 + (float(coord[1]) - centery) ** 2) > (self.cnt.radius + 2 + delta):
                new_coords.append(coord)
        
        for index2 in range(len(new_coords)):
            # convert from list to tuple
            new_coords[index2] = tuple(new_coords[index2])
            
        return new_coords
    
    def xyshift(self, coordinates, x, y):
        """
        Helper function to shift coordinates by x in x-direction and by y in y-direction

        Parameters:
            coordinates [list]: list of tuples that contains xyz coordinates 
            x[float]: shift distance in x direction
            y[float]: shift distance in y direction
        """
        coords = coordinates[0]

        for index in range(len(coords)):
            # convert from tuple to list
            coords[index] = list(coords[index])
        
        for coord in coords:
            coord[0] = "{:.6f}".format(float(coord[0]) + x)
            coord[1] = "{:.6f}".format(float(coord[1]) + y)

        coordinates[0] = coords

        return coordinates
    
    def generate_coords(self, gap, move=0.0):     # I think for the pistion, there should be an option to change the gap between CNT and an outer sheet
                                            # while keeping the other one constant (that's why it's a piston?) so i added a parameter (move)
                                        # tell me if it messes with your vmd tho!
        """
        Returns an list of coordinates, in [x,y,z], representing the piston

        Parameters: 
            gap [float]: distance between 2 outer sheets to each end of CNT
        """
        # generate CNT coordinates
        if self.form == "zig":
            cnt = self.cnt.generate_coords(z=-self.cnt.length*0.5)
        elif self.form == "arm":
            cnt = self.xyshift(self.cnt.generate_coords(),(float(self.sheet.generate_coords()[1]) + float(self.sheet.generate_coords()[2])) / 2,(float(self.sheet.generate_coords()[3]) + float(self.sheet.generate_coords()[4])) / 2)

        sheet1 = self.sheet.generate_coords(-cnt[1] - gap)
        sheet2 = self.sheet.generate_coords(-cnt[1])
        sheet3 = self.sheet.generate_coords(cnt[1])
        sheet4 = self.sheet.generate_coords(cnt[1] + gap + move)
        
        coordinates = sheet1[0] + self.poke(sheet2) + cnt[0] + self.poke(sheet3) + sheet4[0]
        
        return coordinates