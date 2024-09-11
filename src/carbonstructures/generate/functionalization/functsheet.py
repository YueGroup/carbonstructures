from math import sin, cos, radians, sqrt, asin, pi
from .patterns import *
from .groups import *
import copy

__all__ = ['functsheet']

def functsheet(coord_graph):
    """
    Returns a graph containing coordinates and bonds for modified (functionalized) carbon system

    Parameters:
    struct[obj]: an object of the carbon structure to functionalize
    density[float]: R/C coverage density, with R being the functional group
    pattern[str]: functionalized groups patterning: "random", "linear", "patch", or "patterned"
    type[str]: chemical notation for functional group
    """
    funct_coord_graph = copy.deepcopy(coord_graph)

    
        
    return mod_coord

# can have a library for the data of different functional groups
# like bond angles,lengths => coordinates of atoms in different functional groups