import surfaces as surfaces
import sys, getopt
from math import cos, pi

# Gather user input

opts, args = getopt.getopt(sys.argv[1:],"hx:y:l:d:m:g:c:f:")

x = ''
y = ''
l = ''
d = ''
m = 'arm'
g = ''
c = 1.418
f = ''

for opt, arg in opts:
    if opt == '-h':
        print('python generatepiston.py -x <sheet x-length> -y <sheet y-length> -l <cnt length> -d <cnt diameter> (-m <cnt form>) -g <sheet gap size> (-c <cc bond length>) -f <file type>')
        sys.exit()
    elif opt == '-x':
        x = arg
    elif opt == '-y':
        y = arg
    elif opt == '-l':
        l = arg
    elif opt == '-d':
        d = arg
    elif opt == '-m':
        m = arg
    elif opt == '-g':
        g = arg
    elif opt == '-c':
        cc = arg
    elif opt == '-f':
        f = arg

# Exception for missing required inputs

if x == '' or y == '' or l == '' or d == '' or g == '' or f == '':
    raise Exception("Missing required parameters!")

# Generate graphene sheet object with size x, y and bond length c
structure = surfaces.Piston(float(x),float(y),float(l),float(d),m,float(c))

# Define box sizes
xsize = "{:.6f}".format(structure.sheet.xlen)
ysize = "{:.6f}".format(structure.sheet.ylen)
zsize = "{:.6f}".format(structure.cnt.length)
xlo = "{:.6f}".format(-float(c) * cos(pi / 6.0))
xhi = "{:.6f}".format(float(xsize) - float(xlo))
ylo = "0.000000"
yhi = "{:.6f}".format(float(ysize) + float(c))
zlo = "{:.6f}".format(-structure.cnt.length / 2 - float(g))
zhi = "{:.6f}".format(structure.cnt.length / 2 + float(g))
cnthalf = "{:.6f}".format(structure.cnt.length / 2)

coordinates = structure.generate_coords(float(g))
natoms = len(coordinates)

if f == "data":
	# Write LAMMPS data file
	with open('piston_' + str(xsize) + 'by' + str(ysize) + 'by' + str(zsize) + 'type' + m + 'rad' + str(structure.cnt.radius) + '.data','w') as fdata:
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
    with open('piston_' + str(xsize) + 'by' + str(ysize) + 'by' + str(zsize) + 'type' + m + 'rad' + str(structure.cnt.radius) + '.xyz','w') as fdata:
        # Specify number of atoms
        fdata.write('{}\n\n'.format(natoms))
        for pos in coordinates:
            fdata.write('C {} {} {}\n'.format(*pos))

else:
    raise Exception("File format not recognized!")

print("CNT radius: " + str(structure.cnt.radius))
print("Sandwich 1 dimensions:\nx: " + xlo + " " + xhi + "\ny: " + ylo + " " + yhi + "\nz: " + zlo + " -" + cnthalf)
print("Sandwich 1 dimensions:\nx: " + xlo + " " + xhi + "\ny: " + ylo + " " + yhi + "\nz: " + cnthalf + " " + zhi)