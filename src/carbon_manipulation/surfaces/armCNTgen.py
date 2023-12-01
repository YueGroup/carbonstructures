import piston
import armchaircnt

# Generate graphene sheet object with size x,y in Angstroms
armcnt = armchaircnt.ArmCNT(20,10)


# Generate atom positions
#coords = pt.generate_coords_piston(0,0,0,5, 5)
#coords = cnt.generate_coords_zigzag(0,0,0)
#print(coords)

# self =pt
# z=0
# x=0
# y=0
# zL = (z-self.cnt.length*0.5) - 5
# zR = (z+self.cnt.length*0.5) + 5

# # coordinate of bottom-left C atom in graphene sheet
# x_bot = x-self.sheetL.xlen
# y_bot = y-self.sheetL.ylen

#         # generate left and right graphene sheet coordinate
# coord_sheetL = self.sheetL.generate_coords(x_bot,y_bot,zL)
# coord_sheetR = self.sheetR.generate_coords(x_bot,y_bot,zR)
# print(coord_sheetL)
# print(coord_sheetR)


coords = armcnt.generate_coords_armchair()
with open('armcnt_' + str(20) + "by" + str(10) + '.data','w') as fdata:
	# First line is a comment line 
	fdata.write('Atoms for Armchair CNT in LAMMPS\n\n')


	# Write each position 
	for i,pos in enumerate(coords):
		fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))