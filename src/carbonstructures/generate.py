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
    5. Other\n')
    
    system = input()
    
    # Need to fix these to loop until desired output is received
    
    if system == '1':
        structure = gensheet()
        carbons = structure.carbon_graph()
    
    elif system in ['2','3','4']:
        print("Sorry! This is currently unfinished.")
    
    elif system == '5':
        print("Sorry! This package currently does not support the generation of other carbon systems.")
    
    print('Will you be functionalizing this system? Enter Y or N.\n')
    
    # Need to fix these to loop until desired output is received
    
    willfunct = input()
    
    if willfunct == 'Y':
        coordinates = addgroup(carbons)
    
    elif willfunct == 'N':
        coordinates = carbons
    
    print('What would you like to name your data file?\n')
    name = input()
    
    print('What format would you like your data file in?\n \
    1. LAMMPS datafile (.data)\n \
    2. XYZ (.xyz)\n')
    format = input()
    
    nodes = list(coordinates.nodes(data=True))
    if format == '1':
        print('How many total atom types will be in your system?\n')
        atypes = input()
        
        xsize = "{:.6f}".format(structure.xlen)
        ysize = "{:.6f}".format(structure.ylen)
        xlo = "{:.6f}".format(1.418 * cos(pi / 6.0))
        xhi = "{:.6f}".format(float(xsize) - float(xlo))
        ylo = "0.000000"
        yhi = "{:.6f}".format(float(ysize) + 1.418)
        zlo = "0.000000"
        zhi = "0.000000"
        with open(name + '.data','w') as fdata:
            # First line is a comment line 
            fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

            #--- Header ---#
            # Specify number of atoms and atom types 
            fdata.write('{} atoms\n'.format(coordinates.number_of_nodes()))
            fdata.write('{} atom types\n'.format(int(atypes)))
            
            # Specify box dimensions
            fdata.write('{} {} xlo xhi\n'.format(xlo, xhi))
            fdata.write('{} {} ylo yhi\n'.format(ylo, yhi))
            fdata.write('{} {} zlo zhi\n'.format(zlo, zhi))
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