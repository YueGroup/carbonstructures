import carbon_manipulation.surfaces as surfaces
import sys, getopt

from math import cos, pi

# Gather user input

opts, args = getopt.getopt(sys.argv[1:],"hx:y:g:z:c:f:",["length1=","length2=","plane=","coord1","coord2","coord3"])

x = ''
y = ''
g = ''
z = 30
c = 1.418
f = ''

for opt, arg in opts:
    if opt == '-h':
        print('python generatesheet.py -x <x-length> -y <y-length> -g <z-gap size> (-z <z box size>) (-c <cc bond length>) -f <file type>')
        sys.exit()
    elif opt == '-x':
        x = arg
    elif opt == '-y':
        y = arg
    elif opt == '-g':
        g = arg
    elif opt == '-z':
        z = arg
    elif opt == '-c':
        cc = arg
    elif opt == '-f':
        f = arg

# Exception for missing required inputs

if x == '' or y == '' or g == '' or f == '':
    raise Exception("Missing required parameters!")

# Generate graphene sheet object with size x, y and bond length c
structure = surfaces.RectangularSheet(float(x),float(y),float(c))

# Size of the system cell in Angstroms
xsize = "{:.6f}".format(structure.xlen)
ysize = "{:.6f}".format(structure.ylen)
zsize = "{:.6f}".format(float(g) + float(z))
xlo = "{:.6f}".format(-float(c) * cos(pi / 6.0))
xhi = "{:.6f}".format(float(xsize) - float(xlo))
ylo = "0.000000"
yhi = "{:.6f}".format(float(ysize) + float(c))
zlo = "0.000000"
zhi = zsize

coordinates = structure.generate_coords()[0]
coordinates2 = structure.generate_coords(float(g))[0]
natoms = len(coordinates) + len(coordinates2)

if f == "data":
	# Write LAMMPS data file
	with open('sandwich_' + str(xsize) + "by" + str(ysize) + "gapsize" + g + '.data','w') as fdata:
		# First line is a comment line 
		fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

		#--- Header ---#
		# Specify number of atoms and atom types 
		fdata.write('{} atoms\n'.format(natoms))
		fdata.write('{} atom types\n'.format(1))
		# Specify box dimensions
		fdata.write('{} {} xlo xhi\n'.format(xlo, xhi))
		fdata.write('{} {} ylo yhi\n'.format(ylo, yhi))
		fdata.write('{} {} zlo zhi\n'.format(zlo, zhi))
		fdata.write('\n')

		# Atoms section
		fdata.write('Atoms\n\n')

		# Write each position 
		for i,pos in enumerate(coordinates):
			fdata.write('{} 1 1 0 {} {} {}\n'.format(i+1,*pos))

		for i,pos in enumerate(coordinates2):
			fdata.write('{} 1 1 0 {} {} {}\n'.format(i+1,*pos))
			
		# If you have bonds and angles, further sections below

elif f == "xyz":
    # Write XYZ data file
    with open('sandwich_' + str(xsize) + "by" + str(ysize) + "gapsize" + g + '.xyz','w') as fdata:
        # Specify number of atoms
        fdata.write('{}\n\n'.format(natoms))
        for pos in coordinates:
            fdata.write('C {} {} {}\n'.format(*pos))
        for pos in coordinates2:
            fdata.write('C {} {} {}\n'.format(*pos))

else:
    raise Exception("File format not recognized!")