from .surfaces import *
import sys, getopt
from math import cos, pi

__all__ = ['gensheet', 'sheetbox']

def gensheet():
    print('Generating graphene sheet system...\n')
    print('Please enter your system parameters.\n')
    x = float(input('x-direction length: '))
    y = float(input('y-direction length: '))
    
    return RectangularSheet(x,y)

def sheetbox(structure):
    xlo = "{:.6f}".format(-1.418 * cos(pi / 6.0))
    xhi = "{:.6f}".format(float(structure.xlen))
    ylo = "0.000000"
    yhi = "{:.6f}".format(float(structure.ylen))
    zlo = "0.000000"
    zhi = "0.000000"

    return [xlo, xhi, ylo, yhi, zlo, zhi]