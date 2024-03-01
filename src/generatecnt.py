import carbon_manipulation.surfaces as surfaces
import sys, getopt

# opts, args = getopt.getopt(sys.argv[1:],"o:t:p:xyz",["length1=","length2=","plane=","coord1","coord2","coord3"])

if len(sys.argv[1:]) < 3:
    raise Exception("Not enough parameters specified!")

# Generate graphene sheet object with size x,y in Angstroms
if sys.argv[1] == "arm":
    structure = surfaces.ArmchairCNT(float(sys.argv[2]),float(sys.argv[3]))
elif sys.argv[1] == "zig":
    structure = surfaces.ZigzagCNT(float(sys.argv[2]),float(sys.argv[3]))
else:
    pass

# Size of the system cell in Angstroms

coordinates = structure.generate_coords()[0]
natoms = len(coordinates)

if sys.argv[4] == "lammps":
	# Write LAMMPS data file
	with open(sys.argv[1] + 'cnt_diameter' + sys.argv[3] + "length" + sys.argv[2] + '.data','w') as fdata:
		# First line is a comment line 
		fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

		#--- Header ---#
		# Specify number of atoms and atom types 
		fdata.write('{} atoms\n'.format(natoms))
		fdata.write('{} atom type(s)\n'.format(1))
		# Specify box dimensions
		fdata.write('{} {} xlo xhi\n'.format(0.000000, 0.000000))
		fdata.write('{} {} ylo yhi\n'.format(0.000000, 0.000000))
		fdata.write('{} {} zlo zhi\n'.format(0.000000, 0.000000))
		fdata.write('\n')

		# Atoms section
		fdata.write('Atoms\n\n')

		# Write each position 
		for i,pos in enumerate(coordinates):
			fdata.write('{} 3 {} {} {}\n'.format(i+1,*pos))
			
		# If you have bonds and angles, further sections below

elif sys.argv[4] == "xyz":
    # Write XYZ data file
    with open(sys.argv[1] + 'cnt_diameter' + sys.argv[3] + "length" + sys.argv[2] + '.xyz','w') as fdata:
        # Specify number of atoms
        fdata.write('{}\n\n'.format(natoms))
        for pos in coordinates:
            fdata.write('C {} {} {}\n'.format(*pos))

else:
    raise Exception("File format not recognized!")