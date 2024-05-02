from generate import *
import time as t

def main():
    print('Thank you for using the carbonstructures python package! Please respond with the number associated with your choices.\n')
    
    t.sleep(1)
    
    # Prompt the user for some type of input 
    print('What carbon system would you like to generate?\n \
    1. Graphene Sheet\n \
    2. Carbon Nanotube\n \
    3. Graphene Sandwich\n \
    4. Graphene Piston\n \
    5. Other')
    
    system = input()
    
    if system == '5':
        print("Sorry! This package currently does not support the generation of other carbon systems.")
    
    print('What format would you like your data file in?')
    
    format = input()
    
    
    exit = input()

if __name__ == "__main__":
    main()