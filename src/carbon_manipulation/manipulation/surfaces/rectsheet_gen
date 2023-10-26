#-------------------------------------------------------# 
# Generate LAMMPS data file for graphene sheet          #
# 														#
# 	- Nhi Nguyen, October 12, 2023			        	#
#-------------------------------------------------------#
import rectsheet

# Generate graphene sheet object with size x,y in Angstroms
gs = rectsheet.RectangularSheet(10,10)


# Number of atoms to create
natoms = gs.n_Cs

# Size of the system cell in Angstroms
size_x = gs.xlen
size_y = gs.ylen

# Generate atom positions
coords_2d = gs.generate_coords()
# make position 3D by adding z = 0.0
positions=[]
for coord in coords_2d:
	positions.append(coord + (0.0,))
	
# Write LAMMPS data file
with open('rectsheet_' + str(size_x) + "by" + str(size_y) + '.data','w') as fdata:
	# First line is a comment line 
	fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

	#--- Header ---#
	# Specify number of atoms and atom types 
	fdata.write('{} atoms\n'.format(natoms))
	fdata.write('{} atom types\n'.format(1))
	# Specify box dimensions
	fdata.write('{} {} xlo xhi\n'.format(0.0, size_x))
	fdata.write('{} {} ylo yhi\n'.format(0.0, size_y))
	fdata.write('{} {} zlo zhi\n'.format(0.0, 0.0))
	fdata.write('\n')

	# Atoms section
	fdata.write('Atoms\n\n')

	# Write each position 
	for i,pos in enumerate(positions):
		fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))
        
		
	# If you have bonds and angles, further sections below
	