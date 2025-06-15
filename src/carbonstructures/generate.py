from generate import *
from math import sin, cos, pi
import time as ti

def get_min_max(data):
    # Extract numerical positions from the 'pos' attributes
    positions = [tuple(map(float, node_data['pos'])) for _, node_data in data]

    # Unpack x, y, z coordinates
    x_vals, y_vals, z_vals = zip(*positions)
    # print("xvals line 11:" + str(x_vals))
    # print("min(x_vals) line 12:"+ str(min(x_vals)))
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
        ti.sleep(1)
        
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

                        # 1) Remember which nodes were original sheet carbons
                    original_ids = set(carbons.nodes())

                    # 2) Re-build wall1_carbons / wall2_carbons from those originals
                    #    using the true mid-plane of the sheet
                    orig_zs = [float(carbons.nodes[i]['pos'][2]) for i in original_ids]
                    z_mid = (min(orig_zs) + max(orig_zs)) / 2.0

                    wall1_carbons = [(i, coordinates.nodes[i])
                                    for i in original_ids
                                    if float(coordinates.nodes[i]['pos'][2]) <= z_mid]
                    wall2_carbons = [(i, coordinates.nodes[i])
                                    for i in original_ids
                                    if float(coordinates.nodes[i]['pos'][2]) >  z_mid]

                    # 3) Everything not in original_ids is a functional atom
                    all_nodes     = list(coordinates.nodes(data=True))
                    functionals   = [(i, data) for i, data in all_nodes if i not in original_ids]

                    # 4) Assign each functional atom to the nearer wall (by z)
                    w1_avg = sum(float(d['pos'][2]) for _,d in wall1_carbons) / len(wall1_carbons)
                    w2_avg = sum(float(d['pos'][2]) for _,d in wall2_carbons) / len(wall2_carbons)

                    wall1_functionals, wall2_functionals = [], []
                    for i, data in functionals:
                        z = float(data['pos'][2])
                        if abs(z - w1_avg) < abs(z - w2_avg):
                            wall1_functionals.append((i, data))
                        else:
                            wall2_functionals.append((i, data))

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
        # print("bounds line 123:" + str(bounds))
        # print("xlo line 123:" + str(bounds['min_x']))
        format = input()
        while format not in ['1','2']:
            print("Input not recognized! Please enter 1 or 2")
            format = input()

        # Lammps datafile (for simulations)
        if format == '1':
            # Prompt for number of atom types headline
            print("How many total atom types will be in your simulation?\n")
            atypes = input()

            # Prompt for whether water is present
            # Prompt for whether water is present
            while True:
                ans = input("Will there be water in your simulation? Enter Y or N.\n").strip().lower()
                if ans in ('y', 'yes'):
                    # Ask for count
                    while True:
                        cnt = input("How many water molecules will be in the simulation?\n")
                        try:
                            num_water = int(cnt)
                            break
                        except ValueError:
                            print("Please enter a whole number for the water molecule count.")
                    break
                elif ans in ('n', 'no'):
                    num_water = 0
                    break
                else:
                    print("Not a valid answer! Please enter Y or N.")

            
            # Calculate box dimensions
            xlo = "{:.6f}".format(bounds['min_x'])
            xhi = "{:.6f}".format(bounds['max_x'] + structure.CC * cos(pi / 6))
            ylo = "{:.6f}".format(bounds['min_y'])
            yhi = "{:.6f}".format(bounds['max_y'] + structure.CC)
            zlo = "{:.6f}".format(bounds['min_z'])
            zhi = "{:.6f}".format(bounds['max_z'])

            # #print out wallid for lammps input file
            # print ("\n")
            # print("This is the atom id of each wall including the corresponding functional groups on it:")
            # print("(Note: Add water atoms to these ids to get the correct ids (i.e. 4500))")
            # print("Atoms id for wall1: " + "1:" + str(int(coordinates.number_of_nodes()/2)))
            # print("Atoms id for wall2: " + str(int(coordinates.number_of_nodes()/2+1)) + ":" + str(coordinates.number_of_nodes()))
            # #################

            if system == '1':
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

                    #Write each position 
                    for index,data in nodes:
                        fdata.write('{} 1 {} 0 {} {} {}\n'.format(index+1,data['type'][1],*data['pos']))
                    print("wrote line 164")

            elif system == '2':
                    with open(name + '.data','w') as fdata:
                        fdata.write('Atoms for Graphene Sandwich in LAMMPS\n\n')
                        fdata.write('{} atoms\n'.format(coordinates.number_of_nodes()))
                        fdata.write('{} atom types\n'.format(int(atypes)))
                        fdata.write('{} {} xlo xhi\n'.format(xlo, xhi))
                        fdata.write('{} {} ylo yhi\n'.format(ylo, yhi))
                        fdata.write('{} {} zlo zhi\n'.format(zlo, zhi))
                        fdata.write('\nAtoms\n\n')

                        # Build final list: C1 -> F1 -> C2 -> F2
                        final_nodes = wall1_carbons + wall1_functionals + wall2_carbons + wall2_functionals
                        #print(wall1_functionals)
                        #print(wall2_functionals)
                        # Write Atoms section:
                        fdata.write('Atoms\n\n')
                        for new_index, (old_index, data) in enumerate(final_nodes, start=1):
                            fdata.write('{} 1 {} 0 {:.6f} {:.6f} {:.6f}\n'.format(new_index, data['type'][1], *data['pos']))

                        # ────────────────────────────────────────────────────────────
                    # Write a helper “_lammps_info.txt” file
                    info_fname = name + '_lammps_info.txt'
                    with open(info_fname, 'w') as finfo:
                        # 1) Atom‐type → element mapping
                        finfo.write('Atom type mapping:\n')
                        type_map = {}
                        for idx, data in nodes:              # assume `nodes` is list of (id, data) tuples
                            t_id = int(data['type'][1])
                            elem = data['type'][0]
                            type_map[t_id] = elem
                        for t in sorted(type_map):
                            finfo.write(f'  type {t} = {type_map[t]}\n')
                        finfo.write('\n')

                        # 2) Atom ID ranges (offset by water)
                        offset = num_water * 3              # 3 atoms per H2O
                        finfo.write('Atom ID ranges (offset by water) for LAMMPS group commands:\n')
                        if willfunct.upper() == 'Y':
                            # functionalized case: combine walls + functionals

                            # 1) counts
                            n1_c = len(wall1_carbons)
                            n1_f = len(wall1_functionals)
                            n2_c = len(wall2_carbons)
                            n2_f = len(wall2_functionals)

                            # 2) overall sheet ranges (1-based within graphene, then +offset)
                            sheet1_start = offset + 1
                            sheet1_end   = sheet1_start + n1_c + n1_f - 1

                            sheet2_start = sheet1_end + 1
                            sheet2_end   = sheet2_start + n2_c + n2_f - 1

                            # 3) sub‐ranges for C vs F
                            w1_c_start = sheet1_start
                            w1_c_end   = w1_c_start + n1_c - 1

                            w1_f_start = w1_c_end + 1
                            w1_f_end   = sheet1_end

                            w2_c_start = sheet2_start
                            w2_c_end   = w2_c_start + n2_c - 1

                            w2_f_start = w2_c_end + 1
                            w2_f_end   = sheet2_end

                            # 4) write out the groups
                            finfo.write(f'group water      id 1:{offset}\n\n')

                            finfo.write(f'group wall1      id {sheet1_start}:{sheet1_end}\n')
                            finfo.write(f'group wall2      id {sheet2_start}:{sheet2_end}\n\n')

                            finfo.write(f'group wall1_carbons    id {w1_c_start}:{w1_c_end}\n')
                            finfo.write(f'group wall2_carbons    id {w2_c_start}:{w2_c_end}\n\n')

                            finfo.write(f'group wall1_functionals  id {w1_f_start}:{w1_f_end}\n')
                            finfo.write(f'group wall2_functionals  id {w2_f_start}:{w2_f_end}\n')
                        else:
                            # unfunctionalized: split by sheet z
                            zs = [float(d['pos'][2]) for _,d in nodes]
                            zmid = (min(zs) + max(zs)) / 2.0
                            wall1 = [i+offset for i,(i,d) in enumerate(nodes, start=1) if float(d['pos'][2]) <= zmid]
                            wall2 = [i+offset for i,(i,d) in enumerate(nodes, start=1) if float(d['pos'][2]) >  zmid]

                            finfo.write(f'group wall1 id {min(wall1)} {max(wall1)}\n')
                            finfo.write(f'group wall2 id {min(wall2)} {max(wall2)}\n')
                            #finfo.write(f'  all:   {min(wall1)}..{max(wall2)}\n')

                    print(f"Wrote LAMMPS helper info to {info_fname}\n")
                    # ────────────────────────────────────────────────────────────


        # XYZ datafile format (for quick VMD visualization)
        elif format == '2':
            with open(name + '.xyz','w') as fdata:
                fdata.write('{}\n\n'.format(coordinates.number_of_nodes()))
                for index,data in nodes:
                    fdata.write('{} {:.6f} {:.6f} {:.6f}\n'.format(data['type'][0],*data['pos']))

    # Exits the script any time user attempts a keyboard interrupt (Ctrl + C)
    except KeyboardInterrupt:
        print("\nProgram interrupted! Exiting gracefully...")

# Execute program
if __name__ == "__main__":
    main()