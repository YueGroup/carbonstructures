from .surfaces import *
import sys, getopt
from math import cos, pi

__all__ = ['gensheet']

def gensheet():
    print("Generating graphene sheet system...\n")
    print("Please enter your system parameters.\n")
    x = float(input("x-direction length: "))
    y = float(input("y-direction length: "))
    
    return RectangularSheet(x,y)