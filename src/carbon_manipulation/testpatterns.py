import surfaces as s
import functionalization as f
import sys, getopt
from math import cos, pi

# Gather user input

opts, args = getopt.getopt(sys.argv[1:],"hx:y:c:")

x = ''
y = ''
c = 1.418\

for opt, arg in opts:
    if opt == '-h':
        print('python generatesheet.py -x <x-length> -y <y-length> (-c <cc bond length>)')
        sys.exit()
    elif opt == '-x':
        x = arg
    elif opt == '-y':
        y = arg
    elif opt == '-c':
        cc = arg

# Exception for missing required inputs

if x == '' or y == '':
    raise Exception("Missing required parameters!")

# Generate graphene sheet object with size x, y and bond length c
structure = s.RectangularSheet(float(x),float(y),float(c))
carbon_graph = structure.carbon_graph()

# print(f.truerand(carbon_graph))
# print(f.pctrand(carbon_graph,60))
print(f.restrand(carbon_graph))

