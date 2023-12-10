import carbon_manipulation.surfaces as surfaces
import sys, getopt

# opts, args = getopt.getopt(sys.argv[1:],"o:t:p:xyz",["length1=","length2=","plane=","coord1","coord2","coord3"])

if len(sys.argv[1:]) < 3:
    raise Exception("Not enough parameters specified!")

# Generate graphene sheet object with size x,y in Angstroms
structure = surfaces.RectangularSheet(float(sys.argv[1]),float(sys.argv[2]),int(sys.argv[3]))

# Size of the system cell in Angstroms
size1 = structure.len1
size2 = structure.len2

coordinates = structure.generate_coords()
natoms = len(coordinates)

# Write LAMMPS data file
with open('rectsheet_' + str(size1) + "by" + str(size2) + '.data','w') as fdata:
	# First line is a comment line 
	fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

	#--- Header ---#
	# Specify number of atoms and atom types 
	fdata.write('{} atoms\n'.format(natoms))
	fdata.write('{} atom type(s)\n'.format(1))
	# Specify box dimensions
	fdata.write('{} {} xlo xhi\n'.format(0.0, size1))
	fdata.write('{} {} ylo yhi\n'.format(0.0, size2))
	fdata.write('{} {} zlo zhi\n'.format(0.0, 0.0))
	fdata.write('\n')

	# Atoms section
	fdata.write('Atoms\n\n')

	# Write each position 
	for i,pos in enumerate(coordinates):
		fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))
        
		
	# If you have bonds and angles, further sections below