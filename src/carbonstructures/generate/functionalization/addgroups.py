from math import sin, cos, radians, sqrt, asin, pi
from .groups import *
import copy

def addgroup(coord,pattern="truerand",type="OH"):
    """
    Returns a modified list of coordinates with functional groups added onto the structure

    Parameters:
    struct[obj]: an object of the carbon structure to functionalize
    density[float]: R/C coverage density, with R being the functional group
    pattern[str]: functionalized groups patterning: "random", "linear", "patch", or "patterned"
    type[str]: chemical notation for functional group
    """
    mod_coord = copy.deepcopy(coord)

    # select pattern
    #if pattern 

    #elif pattern = 

    #choose C atom to add group (CAN REPLACE WITH GRAPH FUNCTIONS)
    for c in pattern:
        xC = float(coord[c][0])
        yC = float(coord[c][1])
        zC = float(coord[c][2])
    #retrieve bonds and angle data from functional group
        
    return mod_coord

# can have a library for the data of different functional groups
# like bond angles,lengths => coordinates of atoms in different functional groups