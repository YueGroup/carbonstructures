armcnt = armchaircnt.ArmchairCNT(20,10)

coords = armcnt.generate_coords_armchair()
with open('armcnt_' + str(20) + "by" + str(10) + '.data','w') as fdata:
	# First line is a comment line 
	fdata.write('Atoms for Armchair CNT in LAMMPS\n\n')


	# Write each position 
	for i,pos in enumerate(coords):
		fdata.write('{} 1 {} {} {}\n'.format(i+1,*pos))