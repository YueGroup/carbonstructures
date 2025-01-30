# Test script for coverage density of graphene sheets
# run the script from src/carbonstructures, example command in terminal:
#.../src/carbonstructures $ python testing/testcoverage.py -x 10 -y 10 -c 1.42 -p 50

import sys
import getopt
import math
import os

# Automatically add `src/` to Python path so package imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# Import from carbonstructures package
import carbonstructures.generate.surfaces as s
import carbonstructures.generate.functionalization as f

# Gather user input
opts, args = getopt.getopt(sys.argv[1:], "hx:y:c:p:")

x, y, c, p = '', '', 1.418, ''

for opt, arg in opts:
    if opt == '-h':
        print('Usage: python testcoverage.py -x <x-length> -y <y-length> [-c <cc bond length>] [-p <percent coverage>]')
        sys.exit()
    elif opt == '-x':
        x = arg
    elif opt == '-y':
        y = arg
    elif opt == '-c':
        c = arg
    elif opt == '-p':
        p = arg  # Percent functionalization

# Exception for missing required inputs
if x == '' or y == '':
    raise Exception("Missing required parameters for x and y dimensions!")

# Generate graphene sheet object
structure = s.RectangularSheet(float(x), float(y), float(c))
carbon_graph = structure.carbon_graph()

# Check number of nodes and edges
num_nodes = carbon_graph.number_of_nodes()
num_edges = carbon_graph.number_of_edges()

print("\n--- Graphene Sheet Information ---")
print(f"Nodes (C atoms) in the graph: {num_nodes}")
print(f"Edges (bonds) in the graph: {num_edges}")

# Apply functionalization if percentage is specified
if p:
    p = float(p)  # Convert percent input to float
    mod_indices = f.pctrandsheet(carbon_graph, p)  # Apply functionalization

    expected_numC = math.floor((p / 100) * num_nodes)  # Compute expected functionalized sites
    print("\n--- Functionalization Results ---")
    print(f"Coverage: {p}% | Expected: {expected_numC} atoms functionalized, Got: {len(mod_indices)}")

    # Assertion to verify correctness
    assert len(mod_indices) == expected_numC, f"❌ Functionalization failed: Expected {expected_numC}, Got {len(mod_indices)}"

print("\n✅ Test passed successfully!")
