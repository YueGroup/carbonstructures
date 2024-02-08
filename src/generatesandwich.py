import carbon_manipulation.surfaces as surfaces
import sys, getopt

# opts, args = getopt.getopt(sys.argv[1:],"o:t:p:xyz",["length1=","length2=","plane=","coord1","coord2","coord3"])

if len(sys.argv[1:]) < 4:
    raise Exception("Not enough parameters specified!")

# Generate graphene sheet object with size x,y in Angstroms
structure = surfaces.RectangularSheet(float(sys.argv[1]),float(sys.argv[2]))

# Size of the system cell in Angstroms
xsize = "{:.6f}".format(structure.xlen)
ysize = "{:.6f}".format(structure.ylen)
zsize = "{:.6f}".format(float(sys.argv[3]))

coordinates = structure.generate_coords()
coordinates2 = structure.generate_coords(float(sys.argv[3]))
natoms = len(coordinates) + len(coordinates2)

if sys.argv[4] == "lammps":
	# Write LAMMPS data file
	with open('sandwich_' + str(xsize) + "by" + str(ysize) + "gapsize" + str(zsize) + '.data','w') as fdata:
		# First line is a comment line 
		fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

		#--- Header ---#
		# Specify number of atoms and atom types 
		fdata.write('{} atoms\n'.format(natoms))
		fdata.write('{} atom type(s)\n'.format(1))
		# Specify box dimensions
		fdata.write('{} {} xlo xhi\n'.format(0.000000, xsize))
		fdata.write('{} {} ylo yhi\n'.format(0.000000, ysize))
		fdata.write('{} {} zlo zhi\n'.format(0.000000, 0.000000))
		fdata.write('\n')

		# Atoms section
		fdata.write('Atoms\n\n')

		# Write each position 
		for i,pos in enumerate(coordinates):
			fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))

		for i,pos in enumerate(coordinates2):
			fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))
			
		# If you have bonds and angles, further sections below

if sys.argv[4] == "xyz":
    # Write XYZ data file
    with open('sandwich_' + str(xsize) + "by" + str(ysize) + "gapsize" + str(zsize) + '.xyz','w') as fdata:
        # Specify number of atoms
        fdata.write('{}\n\n'.format(natoms))
        for pos in coordinates:
            fdata.write('C {} {} {}\n'.format(*pos))
        for pos in coordinates2:
            fdata.write('C {} {} {}\n'.format(*pos))

else:
    raise Exception("File format not recognized!")