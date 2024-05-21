from math import sin, cos, radians, sqrt, asin, pi, floor
import random

__all__ = ['OH']

def OH(pos):
    CO = 1.47
    OH = 0.98
    COH = radians(107.9)
    O = (pos[0],pos[1],"{:.6f}".format(float(pos[2]) + CO))
    H = ("{:.6f}".format(float(pos[0]) - cos(COH - (pi / 2)) * OH),pos[1],"{:.6f}".format(float(pos[2]) + CO + sin(COH - (pi / 2)) * OH))
    return [[O,'O'],[H,'H']]