from math import sin, cos, radians, sqrt, asin,pi,floor
import random
import copy

# def random_gen(low,high,num):
#     index=[]
#     while len(index)<num+1:
#         n=random.randint(low,high)
#         if n not in index:
#             index.append(n)
#     return index

def addgroup(coord,pattern="truerandom",type="OH"):
    """
    Returns a modified list of coordinates with functional groups added onto the structure

    Parameters:
    struct[obj]: an object of the carbon structure to functionalize
    density[float]: R/C coverage density, with R being the functional group
    pattern[str]: functionalized groups patterning: "random", "linear", "patch", or "patterned"
    type[str]: chemical notation for functional group
    """
    mod_coord = copy.deepcopy(coord)
    #choose C atom to add group (CAN REPLACE WITH GRAPH FUNCTIONS)
    for c in pattern:
        xC = float(coord[c][0])
        yC = float(coord[c][1])
        zC = float(coord[c][2])
    #retrieve bonds and angle data from functional group
        if type=="OH":
            O_coord=[]
            CO=1.47
            OH=0.98
            COH=radians(107.9)
            O_coord = ["{:.6f}".format(xC),"{:.6f}".format(yC),"{:.6f}".format(zC+CO)]

            CH=sqrt(OH*OH+CO*CO-2*OH*CO*cos(COH))
            ang= pi/2-asin(OH*sin(COH)/CH)
            H_coord = ["{:.6f}".format(xC-cos(ang)*CH),"{:.6f}".format(yC),"{:.6f}".format(zC+sin(ang)*CH)]

            mod_coord.append(O_coord)
            mod_coord.append(H_coord)
    return mod_coord



# can have a library for the data of different functional groups
# like bond angles,lengths => coordinates of atoms in different functional groups