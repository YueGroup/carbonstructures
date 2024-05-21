from .functionalization import *
import sys

__all__ = ['addgroup']

# def random_gen(low,high,num):
#     index=[]
#     while len(index)<num+1:
#         n=random.randint(low,high)
#         if n not in index:
#             index.append(n)
#     return index

patterns = {
    '1': truerand,
    '2': pctrand,
    '3': restrand
}

groups = {
    '1': OH
}

def addgroup(coord):
    print('Please select a functional group pattern:\n \
    1. True Random\n \
    2. Percent Random\n \
    3. Restricted Random\n')
    
    patternkey = input()

    while patternkey not in list(patterns.keys()):
        if patternkey == 'exit()':
            sys.exit
        print("Input not recognized! Please select an available option: ")
        patternkey = input()
    
    pattern = patterns.get(patternkey)(coord)

    print('Please select a functional group type:\n \
    1. OH\n')

    groupkey = input()

    while groupkey not in list(groups.keys()):
        if groupkey == 'exit()':
            sys.exit
        print("Input not recognized! Please select an available option: ")
        groupkey = input()

    for index in pattern:
        groupcoords = groups.get(groupkey)(coord.nodes[index]['pos'])
        for node in range(len(groupcoords)):
            coord.add_node(int(max(coord.nodes)) + 1, pos=groupcoords[node][0], type=[groupcoords[node][1],str(2 + node)])
            
    return coord
        
    



# can have a library for the data of different functional groups
# like bond angles,lengths => coordinates of atoms in different functional groups