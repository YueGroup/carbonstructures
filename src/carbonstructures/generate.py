from generate import *
from math import sin, cos, pi
import time as t

def get_min_max(data):
    # Extract numerical positions from the 'pos' attributes
    positions = [tuple(map(float, node_data['pos'])) for _, node_data in data]

    # Unpack x, y, z coordinates
    x_vals, y_vals, z_vals = zip(*positions)

    # Compute min and max values
    return {
        'min_x': min(x_vals), 'max_x': max(x_vals),
        'min_y': min(y_vals), 'max_y': max(y_vals),
        'min_z': min(z_vals), 'max_z': max(z_vals)
    }

def main():
    try:
        # Program start-up
        print("Thank you for using the carbonstructures python package!\n")
        t.sleep(1)
        
        # Prompts user to select a carbon structure
        print("What carbon system would you like to generate?\n \
        1. Graphene Sheet\n \
        2. Graphene Sandwich\n \
        3. Carbon Nanotube\n \
        4. Graphene Piston")
        
        # Loops through until valid system is chosen
        system = input()
        while system not in ['1', '2']: 
            # Unfinished features: carbon nanotube and graphene piston
            if system in ['3','4']:
                print("\nSorry! This is currently unfinished. Please try again.")
            # Unrecognized input
            else:
                print("\nInput not recognized! Please try again.")
            # Re-prompt user
            system = input()

        # Generates chosen system and stores system object as 'structure'
        if system == '1':
            structure = gensheet()
        elif system == '2':
            structure = gensandwich()
        # Generates structure coordinates in graph form
        carbons = structure.carbon_graph()

        # Prompt user to functionalize system
        print("Will you be functionalizing this system? Enter Y or N.\n")
        
        # Loops through until user chooses (not) to functionalize the structure
        willfunct = input()
        while willfunct not in ['Y','N']:
            print("\nInput not recognized! Please try again.")
            willfunct = input()
        
        # Generates functionalized coordinates in graph form and stores as 'coordinates'
        if willfunct == 'Y':
            if system in ['1']:
                    coordinates = functsheet(carbons)
            elif system in ['2']:
                    coordinates = functsandwich(carbons)
            else:
                    print("\nSorry! We currently do not support functionalization of the system you chose.")

        # Stores unfunctionalized coordinate graph as 'coordinates'
        elif willfunct == 'N':
                coordinates = carbons
        
        # Prompt user for file name
        print("\nWhat would you like to name your data file?\n")
        name = input()
        
        # Prompt user for file type
        print("\nWhat format would you like your data file in?\n \
        1. LAMMPS datafile (.data)\n \
        2. XYZ (.xyz)\n")

        # Select graph nodes as list of coordinates. Loop until valid file format is chosen
        nodes = list(coordinates.nodes(data=True))
        bounds = get_min_max(nodes)
        format = input()
        while format not in ['1','2']:
            print("Input not recognized! Please enter 1 or 2")
            format = input()

        # Lammps datafile (for simulations)
        if format == '1':
            # Prompt for number of atom types headline
            print("How many total atom types will be in your simulation?\n")
            atypes = input()
            
            # Calculate box dimensions
            xlo = "{:.6f}".format(bounds['min_x'])
            xhi = "{:.6f}".format(bounds['max_x'] + structure.CC * cos(pi / 6))
            ylo = "{:.6f}".format(bounds['min_y'])
            yhi = "{:.6f}".format(bounds['max_y'] + structure.CC)
            zlo = "{:.6f}".format(bounds['min_z'])
            zhi = "{:.6f}".format(bounds['max_z'])

            #print out wallid for lammps input file
            print ("\n")
            print("This is the atom id of each wall including the corresponding functional groups on it:")
            print("(Note: Add water atoms to these ids to get the correct ids (i.e. 4500))")
            print("Atoms id for wall1: " + "1:" + str(int(coordinates.number_of_nodes()/2)))
            print("Atoms id for wall2: " + str(int(coordinates.number_of_nodes()/2+1)) + ":" + str(coordinates.number_of_nodes()))
        
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
                # for index,data in nodes:
                #     fdata.write('{} 1 {} 0 {} {} {}\n'.format(index+1,data['type'][1],*data['pos']))
                # Sort by z-coordinate, then node index
                sorted_nodes = sorted(
                    coordinates.nodes(data=True),
                    key=lambda item: (float(item[1]['pos'][2]), item[0])
                )

                # Write each position 
                for new_index, (old_index, data) in enumerate(sorted_nodes, start=1):
                    fdata.write('{} 1 {} 0 {} {} {}\n'.format(new_index, data['type'][1], *data['pos']))
                
        
        # XYZ datafile format (for quick VMD visualization)
        elif format == '2':
            with open(name + '.xyz','w') as fdata:
                fdata.write('{}\n\n'.format(coordinates.number_of_nodes()))
                # for index,data in nodes:
                #     fdata.write('{} {} {} {}\n'.format(data['type'][0],*data['pos']))

                # Sort by z-coordinate, then by node index to preserve order
                sorted_nodes = sorted(
                    coordinates.nodes(data=True),
                    key=lambda item: (float(item[1]['pos'][2]), item[0])
                )

                for _, data in sorted_nodes:
                    fdata.write('{} {} {} {}\n'.format(data['type'][0], *data['pos']))

    # Exits the script any time user attempts a keyboard interrupt (Ctrl + C)
    except KeyboardInterrupt:
        print("\nProgram interrupted! Exiting gracefully...")

# Execute program
if __name__ == "__main__":
    main()