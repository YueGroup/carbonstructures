from carbon_manipulation.functionalization import addgroups
import carbon_manipulation.surfaces as surfaces
import sys, getopt
from math import cos, pi

# Gather user input

opts, args = getopt.getopt(sys.argv[1:],"hx:y:c:f:")

x = ''
y = ''
c = 1.418
f = ''

for opt, arg in opts:
    if opt == '-h':
        print('python generatesheet.py -x <x-length> -y <y-length> (-c <cc bond length>) -f <file type>')
        sys.exit()
    elif opt == '-x':
        x = arg
    elif opt == '-y':
        y = arg
    elif opt == '-c':
        cc = arg
    elif opt == '-f':
        f = arg

# Exception for missing required inputs

if x == '' or y == '' or f == '':
    raise Exception("Missing required parameters!")

# Generate graphene sheet object with size x, y and bond length c
structure = surfaces.RectangularSheet(float(x),float(y),float(c))


# Define box sizes
# MAKE BOX SIZE HUGE (THIS NOT THE RIGHT SIZE)
xsize = "{:.6f}".format(100)
ysize = "{:.6f}".format(100)
xlo = "{:.6f}".format(-20)
xhi = "{:.6f}".format(30)
ylo = "-20"
yhi = "{:.6f}".format(30)
zlo = "0.000000"
zhi = "20"

#NUMBER OF ATOMS INCREASES
coordinates = structure.generate_coords()[0]
new = addgroups.addgroup(coordinates,0.25)
natoms = len(new)
print(natoms)

if f == "data":
	# Write LAMMPS data file
	with open('rectsheet_' + str(xsize) + "by" + str(ysize) + '.data','w') as fdata:
		# First line is a comment line 
		fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

		#--- Header ---#
		# Specify number of atoms and atom types 
		fdata.write('{} atoms\n'.format(natoms))
		fdata.write('{} atom type(s)\n'.format(1))
		# Specify box dimensions
		fdata.write('{} {} xlo xhi\n'.format(xlo, xhi))
		fdata.write('{} {} ylo yhi\n'.format(ylo, yhi))
		fdata.write('{} {} zlo zhi\n'.format(zlo, zhi))
		fdata.write('\n')

		# Atoms section
		fdata.write('Atoms\n\n')

		# Write each position 
		for i,pos in enumerate(coordinates):
			fdata.write('{} 3 {} {} {}\n'.format(i+1,*pos))
			
		# If you have bonds and angles, further sections below

elif f == "xyz":
    # Write XYZ data file
    with open('testsheet' + '.xyz','w') as fdata:
        # Specify number of atoms
        fdata.write('{}\n\n'.format(natoms))
        for pos in new[:len(coordinates)]:
            fdata.write('C {} {} {}\n'.format(*pos))

        it=iter(new[len(coordinates):])
        for pos1,pos2 in zip(it,it):
            fdata.write('O {} {} {}\n'.format(*pos1))
            fdata.write('H {} {} {}\n'.format(*pos2))

else:
    raise Exception("File format not recognized!")