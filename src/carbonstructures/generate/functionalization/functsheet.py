from math import sin, cos, radians, sqrt, asin, pi
from .patterns import *
from .groups import *
import copy

__all__ = ['functsheet']

def functsheet(coord_graph):
    print('Functionalizing graphene sheet system...\n')
    print('What functional group would you like to add?\n')
    grp = input()

    funct_coord_graph = copy.deepcopy(coord_graph)

    
        
    return mod_coord

# can have a library for the data of different functional groups
# like bond angles,lengths => coordinates of atoms in different functional groups