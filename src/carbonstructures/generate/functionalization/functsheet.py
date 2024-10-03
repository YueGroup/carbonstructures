from math import sin, cos, radians, sqrt, asin, pi
from .patterns import *
from .groups import *
import copy

__all__ = ['functsheet']

def functsheet(coord_graph):
    print("Functionalizing graphene sheet system...\n")

    # Prompt user to select a functional group
    print("What group would you like to functionalize with? Type 'groups' to see all supported functional groups.\n")
    grps = list(grpdata.keys())
    grp = input()

    # Loop until valid functional group is chosen
    while grp not in grps: 
        if grp == 'groups':
            print(str(grps) + "\n")
            print("Please choose a group to functionalize the system with.\n")

        else: 
            print("Input not recognized! Please try again.\n")

        grp = input()
    
    # Prompt user to select a functionalization pattern
    print("What functionalization pattern would you like to use? Type 'patterns' to see all supported patterns.\n \
        1. True Random\n \
        2. Random - Percent Coverage\n \
        3. Random - Restricted Coverage\n")
    patternlist = [truerandsheet, pctrandsheet, restrandsheet]
    pattern = input()
    
    # Loop until valid pattern is chosen
    while pattern not in ['1','2','3']:
        print("Input not recognized! Please try again.\n")
        pattern = input()

    # Get list of carbon indices to functionalize
    if pattern == '2':
        while True:
            pct_input = input("Please specify a coverage percentage between 0 and 100: ")
            
            try:
                # Try to convert the input to a float
                cov_pct = float(pct_input)
                break 
            except ValueError:
                # If conversion fails, the input is not a number 
                print("That's not a valid number. Please try again.")
        mod_indices = patternlist[int(pattern) - 1](coord_graph,cov_pct)
    
    else:
        mod_indices = patternlist[int(pattern) - 1](coord_graph)

    mod_coord_graph = copy.deepcopy(coord_graph)
    functdata = list(grpdata[grp])

    for index in mod_indices:
        c_coords = mod_coord_graph.nodes[index]['pos']

        # Functional group with 1 atom (perpendicular to sheet)
        if grpdata[grp][functdata[0]] == 1:
            x1 = c_coords[0]
            y1 = c_coords[1]
            z1 = "{:.6f}".format(float(c_coords[2]) + grpdata[grp][functdata[1]]['length'])
            mod_coord_graph.add_node(mod_coord_graph.number_of_nodes(), pos=(x1,y1,z1), type=grpdata[grp][functdata[1]]['added_atom'])

        # Functional group with 2 atoms
            # Calculate coordinates and add node for atom 1
        if grpdata[grp][functdata[0]] == 2:
            x1 = c_coords[0]
            y1 = c_coords[1]
            z1 = "{:.6f}".format(float(c_coords[2]) + grpdata[grp][functdata[1]]['length'])
            mod_coord_graph.add_node(mod_coord_graph.number_of_nodes(), pos=(x1,y1,z1), type=grpdata[grp][functdata[1]]['added_atom'])

            # Calculate coordinates and add node for atom 2

            x2 = "{:.6f}".format(float(c_coords[0]) - grpdata[grp][functdata[2]]['length'] * cos(radians(grpdata[grp][functdata[2]]['angle'] - 90)))
            y2 = c_coords[1]
            z2 = "{:.6f}".format(float(z1) + grpdata[grp][functdata[2]]['length'] * sin(radians(grpdata[grp][functdata[2]]['angle'] - 90)))
            mod_coord_graph.add_node(mod_coord_graph.number_of_nodes(), pos=(x2,y2,z2), type=grpdata[grp][functdata[2]]['added_atom'])

    return mod_coord_graph