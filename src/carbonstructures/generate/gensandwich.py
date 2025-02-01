from .surfaces import *
import sys, getopt
from math import cos, pi

__all__ = ['gensandwich']

# Helper function to get numeric input from user
def get_numeric_input(prompt, allow_default=False, default_value=1.418):
    while True:
        value = input(prompt)
        if allow_default and value.lower() == 'default':
            return default_value
        try:
            return float(value)
        except ValueError:
            print("That's not a valid number. Please try again.")

def gensandwich():
    # Prompt start-up
    print("Generating graphene sheet system...\n")
    print("Please enter your system parameters.\n")
    
    # Get input values
    x = get_numeric_input("x-direction length (Angstroms): ")
    y = get_numeric_input("y-direction length (Angstroms): ")
    g = get_numeric_input("Gap size (Angstroms): ")
    cc = get_numeric_input("C-C bond length (Angstroms). Type 'default' to use the default length, 1.418: ", allow_default=True)
    
    # Returns rectangular sheet object
    return Sandwich(x, y, g, cc)