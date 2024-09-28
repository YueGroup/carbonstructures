from math import sin, cos, radians, sqrt, asin, pi
from .patterns import *
from .groups import *
import copy
import networkx as nx

__all__ = ['functsandwich']

def functsandwich(coord_graph):
    print("Functionalizing graphene sandwich system...\n")

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
    patternlist = [truerand, pctrand, restrand]
    pattern = input()
    
    # Loop until valid pattern is chosen
    while pattern not in ['1','2','3']:
        print("Input not recognized! Please try again.\n")
        pattern = input()

    # Get list of carbon indices to functionalize
    if pattern == '2':
        while True:
            pct_input = input("Please specify a coverage percentage: ")
            
            try:
                # Try to convert the input to a float
                cov_pct = float(pct_input)
                break 
            except ValueError:
                # If conversion fails, the input is not a number 
                print("That's not a valid number. Please try again.")

        ## need to fix
        graph = copy.copy(coord_graph)
        slice1= nx.subgraph(coord_graph,range(0,int(nx.number_of_nodes(graph)/2)))
        slice2= nx.subgraph(coord_graph,range(int(nx.number_of_nodes(graph)/2),int(nx.number_of_nodes(graph))))
        print(slice1)
        print(slice2)
        mod_indice1 = patternlist[int(pattern) - 1](slice1,cov_pct)
        print(mod_indice1)
        mod_indice2 = patternlist[int(pattern) - 1](slice2,cov_pct)
        print(mod_indice2)
        mod_indices = mod_indice1 + mod_indice2
        print(mod_indices)
        ##
    
    else:
        mod_indices = patternlist[int(pattern) - 1](coord_graph)
    
    print(mod_indices)

    mod_coord_graph = copy.deepcopy(coord_graph)
    functdata = list(grpdata[grp])
    print(mod_coord_graph.nodes[2])
    print(grpdata[grp][functdata[0]])
   
    for index in mod_indices:
        print(index)
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

            # print(str(mod_coord_graph.number_of_nodes()))
            # print(str((x1,y1,z1)))
            # print(str(grpdata[grp][functdata[1]]['added_atom']))
            mod_coord_graph.add_node(mod_coord_graph.number_of_nodes(), pos=(x1,y1,z1), type=grpdata[grp][functdata[1]]['added_atom'])

            # Calculate coordinates and add node for atom 2

            x2 = "{:.6f}".format(float(c_coords[0]) - grpdata[grp][functdata[2]]['length'] * cos(radians(grpdata[grp][functdata[2]]['angle'] - 90)))
            y2 = c_coords[1]
            z2 = "{:.6f}".format(float(z1) + grpdata[grp][functdata[2]]['length'] * sin(radians(grpdata[grp][functdata[2]]['angle'] - 90)))

            mod_coord_graph.add_node(mod_coord_graph.number_of_nodes(), pos=(x2,y2,z2), type=grpdata[grp][functdata[2]]['added_atom'])
    
    print(coord_graph)
    print(mod_coord_graph)
    return mod_coord_graph