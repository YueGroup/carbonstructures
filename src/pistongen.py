
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from carbon_manipulation.surfaces.piston import Piston

# List of (x, y, z) coordinates
structure = Piston("zigzag",10,3,5,5)
points = structure.generate_coords(dist_left=5.0, dist_right=5.0)

with open('piston' + '.data','w') as fdata:
		# First line is a comment line 
		fdata.write('Atoms for Graphene Sheet in LAMMPS\n\n')

		#--- Header ---#
		
		# Atoms section
		fdata.write('Atoms\n\n')

		# Write each position 
		for i,pos in enumerate(points):
			fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))
			
# # Separate x, y, z coordinates 
# x_coords, y_coords, z_coords = zip(*points)

# # Create a 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot points
# ax.scatter(x_coords, y_coords, z_coords, c='r', marker='o')

# # Set labels
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

# # Show plot
# plt.show()
