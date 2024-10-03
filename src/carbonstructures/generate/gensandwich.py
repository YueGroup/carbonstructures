from .surfaces import *
import sys, getopt
from math import cos, pi

__all__ = ['gensandwich']

def gensandwich():
    print("Generating graphene sandwich system...\n")
    print("Please enter your system parameters.\n")
    x = float(input("x-direction length: "))
    y = float(input("y-direction length: "))
    g = float(input("Gap size: "))

    return Sandwich(x,y,g)