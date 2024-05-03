from .surfaces import *
import sys, getopt
from math import cos, pi

__all__ = ['gensheet']

def gensheet():
    print('Generating graphene sheet system...\n')
    print('Please enter your system parameters.\n')
    x = float(input('x-direction length: '))
    y = float(input('y-direction length: '))
    
    return RectangularSheet(x,y)

# # Gather user input

# opts, args = getopt.getopt(sys.argv[1:],"hx:y:c:f:")

# x = ''
# y = ''
# c = 1.418
# f = ''

# for opt, arg in opts:
#     if opt == '-h':
#         print('python generatesheet.py -x <x-length> -y <y-length> (-c <cc bond length>) -f <file type>')
#         sys.exit()
#     elif opt == '-x':
#         x = arg
#     elif opt == '-y':
#         y = arg
#     elif opt == '-c':
#         cc = arg
#     elif opt == '-f':
#         f = arg

# # Exception for missing required inputs

# if x == '' or y == '' or f == '':
#     raise Exception("Missing required parameters!")

# # Generate graphene sheet object with size x, y and bond length c
# structure = surfaces.RectangularSheet(float(x),float(y),float(c))

# # Define box sizes
# xsize = "{:.6f}".format(structure.xlen)
# ysize = "{:.6f}".format(structure.ylen)
# xlo = "{:.6f}".format(-float(c) * cos(pi / 6.0))
# xhi = "{:.6f}".format(float(xsize) - float(xlo))
# ylo = "0.000000"
# yhi = "{:.6f}".format(float(ysize) + float(c))
# zlo = "0.000000"
# zhi = "0.000000"

# coordinates = structure.generate_coords()[0]
# natoms = len(coordinates)

# if f == "data":
# 	# Write LAMMPS data file
# 	with open('rectsheet_' + str(xsize) + "by" + str(ysize) + '.data','w') as fdata:
# 		# First line is a comment line 
# 		fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

# 		#--- Header ---#
# 		# Specify number of atoms and atom types 
# 		fdata.write('{} atoms\n'.format(natoms))
# 		fdata.write('{} atom type(s)\n'.format(1))
# 		# Specify box dimensions
# 		fdata.write('{} {} xlo xhi\n'.format(xlo, xhi))
# 		fdata.write('{} {} ylo yhi\n'.format(ylo, yhi))
# 		fdata.write('{} {} zlo zhi\n'.format(zlo, zhi))
# 		fdata.write('\n')

# 		# Atoms section
# 		fdata.write('Atoms\n\n')

# 		# Write each position 
# 		for i,pos in enumerate(coordinates):
# 			fdata.write('{} 3 {} {} {}\n'.format(i+1,*pos))
			
# 		# If you have bonds and angles, further sections below

# elif f == "xyz":
#     # Write XYZ data file
#     with open('rectsheet_' + str(xsize) + "by" + str(ysize) + '.xyz','w') as fdata:
#         # Specify number of atoms
#         fdata.write('{}\n\n'.format(natoms))
#         for pos in coordinates:
#             fdata.write('C {} {} {}\n'.format(*pos))

# else:
#     raise Exception("File format not recognized!")