from generate import *
import time as t

def main():
    try:
        print("Thank you for using the carbonstructures python package!\n")

        t.sleep(1)
        
        # Prompt user to select a carbon structure
        print("What carbon system would you like to generate?\n \
        1. Graphene Sheet\n \
        2. Carbon Nanotube\n \
        3. Graphene Sandwich\n \
        4. Graphene Piston")
        
        # Loop until valid system is chosen
        system = '0'
        while system not in ['1']: 
            system = input()

            if system == '1':
                structure = gensheet()
                carbons = structure.carbon_graph()
        
            elif system in ['2','3','4']:
                print("\nSorry! This is currently unfinished. Please try again.")
            
            else:
                print("\nInput not recognized! Please try again.")

        # Prompt user to functionalize system
        print("Will you be functionalizing this system? Enter Y or N.\n")
        
        # Loop until user chooses (not) to functionalize the structure
        willfunct = '0'
        while willfunct not in ['Y','N']:
            willfunct = input()

            if willfunct == 'Y':
                if system in ['1']:
                    coordinates = functsheet(carbons)

                else:
                    print("\nSorry! We currently do not support functionalization of the system you chose.")

            elif willfunct == 'N':
                coordinates = carbons

            else:
                print("\nInput not recognized! Please try again.")
        
        # Prompt user for file name
        print('\nWhat would you like to name your data file?\n')
        name = input()
        
        # Prompt user for file type
        print('\nWhat format would you like your data file in?\n \
        1. LAMMPS datafile (.data)\n \
        2. XYZ (.xyz)\n')

        # Select graph nodes as list of coordinates. Loop until valid file format is chosen
        nodes = list(coordinates.nodes(data=True))
        format = '0'
        while format not in ['1','2']:
            format = input()

            # Lammps datafile (for simulations)
            if format == '1':
                # Prompt for number of atom types headline
                print('How many total atom types will be in your simulation?\n')
                atypes = input()
                
                # Calculate box dimensions
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
            
            # XYZ datafile format (for quick VMD visualization)
            elif format == '2':
                with open(name + '.xyz','w') as fdata:
                    fdata.write('{}\n\n'.format(coordinates.number_of_nodes()))
                    for index,data in nodes:
                        fdata.write('{} {} {} {}\n'.format(data['type'][0],*data['pos']))
            
            else:
                print("Input not recognized! Please enter 1 or 2")
    
    except KeyboardInterrupt:
        print("\nProgram interrupted! Exiting gracefully...")

# Execute program
if __name__ == "__main__":
    main()