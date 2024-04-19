import surfaces as s
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
        cc = arg\

# Exception for missing required inputs

if x == '' or y == '':
    raise Exception("Missing required parameters!")

# Generate graphene sheet object with size x, y and bond length c
structure = s.RectangularSheet(float(x),float(y),float(c))
carbon_graph = structure.carbon_graph()

print("Nodes in the graph:", list(carbon_graph.nodes))
print("Edges in the graph:", list(carbon_graph.edges))
print("Number of nodes:", carbon_graph.number_of_nodes())
print("Number of edges:", carbon_graph.number_of_edges())