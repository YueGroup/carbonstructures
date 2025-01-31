from .surfaces import *
import sys, getopt
from math import cos, pi

__all__ = ['gensheet']

def gensheet():
    print("Generating graphene sheet system...\n")
    print("Please enter your system parameters.\n")
    x = float(input("x-direction length: "))
    y = float(input("y-direction length: "))
    cc = input("C-C bond length in Angstrom: ")
    if cc == 'default':
        return RectangularSheet(x,y)
    else:
        return RectangularSheet(x,y,float(cc))