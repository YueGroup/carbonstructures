from generate import *
from modify import *
import time as t
import sys

def main():
    print('Thank you for using the carbonstructures python package! Enter exit() at any time to exit.\n')
    
    t.sleep(1)
    
    # Prompt for structure generation
    print('What carbon system would you like to generate?\n \
    1. Graphene Sheet\n \
    2. Carbon Nanotube\n \
    3. Graphene Sandwich\n \
    4. Graphene Piston\n \
    5. Other\n')

    system = input()

    # Non-generation options
    while system not in ['1','2','3','4']:
        if system == 'exit()':
            sys.exit()
        elif system == '5':
            print("Sorry! This package does not currently support the generation of other structures. Please select another option or type 'exit()' to exit.")
        else:
            print("Input not recognized! Please select an available option: ")
        system = input()
    
    # Generation options
    if system == '1':
        structure = gensheet()
        box = sheetbox(structure)
    
    elif system in ['2','3','4']:
        print("This option is currently unfinished.")
        sys.exit()
    
    # Prompt for functionalization
    print('Will you be functionalizing this system?\n')
    
    willfunct = input()

    # Unavailable options
    while willfunct not in ['Y','N']:
        if willfunct == 'exit()':
            sys.exit()
        else:
            print("Input not recognized! Please select an available option: ")
        willfunct = input()
    
    # Functionalization options
    if willfunct == 'Y':
        coordinates = addgroup(structure.carbon_graph())
    
    elif willfunct == 'N':
        coordinates = structure.carbon_graph()
    
    print('What would you like to name your data file?\n')
    name = input()
    
    print('What format would you like your data file in?\n \
    1. LAMMPS datafile (.data)\n \
    2. XYZ (.xyz)\n')
    format = input()
    
    while format not in ['1','2']:
        if format == 'exit()':
            sys.exit()
        else:
            print("Input not recognized! Please select an available option: ")
        format = input()

    nodes = list(coordinates.nodes(data=True))
    if format == '1':
        print('How many total atom types will be in your system?\n')
        atypes = input()
        with open(name + '.data','w') as fdata:
            # First line is a comment line 
            fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

            #--- Header ---#
            # Specify number of atoms and atom types 
            fdata.write('{} atoms\n'.format(coordinates.number_of_nodes()))
            fdata.write('{} atom types\n'.format(int(atypes)))
                
            # Specify box dimensions
            fdata.write('{} {} xlo xhi\n'.format(box[0], box[1]))
            fdata.write('{} {} ylo yhi\n'.format(box[2], box[3]))
            fdata.write('{} {} zlo zhi\n'.format(box[4], box[5]))
            fdata.write('\n')

            # Atoms section
            fdata.write('Atoms\n\n')

            # Write each position 
            for index,data in nodes:
                fdata.write('{} 1 {} 0 {} {} {}\n'.format(index+1,data['type'][1],*data['pos']))
    elif format == '2':
        with open(name + '.xyz','w') as fdata:
            fdata.write('{}\n\n'.format(coordinates.number_of_nodes()))
            for index,data in nodes:
                fdata.write('{} {} {} {}\n'.format(data['type'][0],*data['pos']))
    else:
        print("Input not recognized! Please enter 1 or 2") 
    
if __name__ == "__main__":
    main()