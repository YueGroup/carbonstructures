import math
import networkx as nx
import copy
from .patterns import truerandsheet, pctrandsandwich, restrandsheet
from .groups import grpdata

__all__ = ['functsandwich']


def build_group_graph(group_name: str) -> nx.DiGraph:
    """
    Build a directed graph of a functional group, rooted at 'base'.
    Each node has a 'pos' attribute giving its (x,y,z) offset from the base carbon.
    Uses each atom's 'length', 'angle', and 'dihedral' from grpdata.
    """
    info = grpdata[group_name]
    G = nx.DiGraph()
    # Base carbon at the origin
    G.add_node('base', type='C', pos=(0.000000,0.000000,0.000000))

    def children_of(parent):
        return [k for k,v in info.items() if k != 'atoms' and v['parent'] == parent]

    def recurse(parent):
        px, py, pz = G.nodes[parent]['pos']
        for child in children_of(parent):
            atom = info[child]
            L = float(atom['length'])
            θ = math.radians(atom.get('angle', 0.0))
            ϕ = math.radians(atom.get('dihedral', 0.0))
            # For the first bond from base, go along +z
            if parent == 'base':
                dx, dy, dz = 0.0, 0.0, L
            else:
                dx = L * math.cos(θ) * math.cos(ϕ)
                dy = L * math.cos(θ) * math.sin(ϕ)
                dz = L * math.sin(θ)
            new_pos = (round(px + dx,6), round(py + dy,6), round(pz + dz,6))
            G.add_node(child, type=atom['added_atom'], pos=new_pos)
            G.add_edge(parent, child)
            recurse(child)

    recurse('base')
    return G


def attach_group(
    coord_graph: nx.Graph,
    group_name: str,
    base_indices: list
) -> nx.Graph:
    """
    Attach functional groups so they point into the sandwich gap.

    - Flatten any nested lists in base_indices.
    - Parse all existing node positions to floats.
    - Compute the sandwich mid-plane z = (min_z + max_z)/2.
    - For each base carbon index:
      • Determine sign = -1 if its z > mid-plane (top sheet), else +1.
      • Copy every atom from group graph, translating x,y by child offsets and z by sign * child_z.
    """
    # Copy original graph
    Gnew = coord_graph.copy()

    # Flatten base indices
    flat_indices = []
    for idx in base_indices:
        if isinstance(idx, (list, tuple)):
            flat_indices.extend(idx)
        else:
            flat_indices.append(idx)

    # Parse and normalize node positions to float triples
    for node, data in Gnew.nodes(data=True):
        raw_pos = data.get('pos')
        if isinstance(raw_pos, str):
            parts = raw_pos.strip('()[]').split(',')
            coords = tuple(map(float, parts))
        else:
            coords = tuple(map(float, raw_pos))
        Gnew.nodes[node]['pos'] = coords

    # Compute mid-plane z from normalized positions
    zs = [pos[2] for _, pos in nx.get_node_attributes(Gnew, 'pos').items()]
    mid_z = (min(zs) + max(zs)) / 2.0

    # Build the group graph using default lengths (e.g. CH3 C–C = 1.54 Å)
    Ggrp = build_group_graph(group_name)
    next_id = max(Gnew.nodes) + 1

    for base_idx in flat_indices:
        if base_idx not in Gnew.nodes:
            raise KeyError(f"Base index {base_idx} not found in graph nodes")
        bx, by, bz = Gnew.nodes[base_idx]['pos']
        sign = -1.0 if bz > mid_z else +1.0
        mapping = {'base': base_idx}

        # Add each non-base atom
        for node in nx.topological_sort(Ggrp):
            if node == 'base':
                continue
            rx, ry, rz = Ggrp.nodes[node]['pos']
            abs_pos = (round(bx + rx,6), round(by + ry,6), round(bz + sign * rz,6))
            Gnew.add_node(next_id,
                          pos=abs_pos,
                          type=Ggrp.nodes[node]['type'])
            mapping[node] = next_id
            next_id += 1

        # Add bonds
        for u, v in Ggrp.edges():
            Gnew.add_edge(mapping[u], mapping[v])

    return Gnew


def functsandwich(coord_graph):
    print("Functionalizing graphene sandwich system...\n")

    # Prompt user to select a functional group
    print("What group would you like to functionalize with? Type 'groups' to see all supported functional groups.\n")
    grps = list(grpdata.keys())
    grp = input().strip()

    # Loop until valid functional group is chosen
    while grp not in grps:
        if grp == 'groups':
            print(str(grps) + "\n")
            print("Please choose a group to functionalize the system with.\n")
        else:
            print("Input not recognized! Please try again.\n")
        grp = input().strip()
    
    # Prompt user to select a functionalization pattern
    print("What functionalization pattern would you like to use? Type 'patterns' to see all supported patterns.\n        1. True Random\n        2. Random - Percent Coverage\n        3. Random - Restricted Coverage\n")
    patternlist = [truerandsheet, pctrandsandwich, restrandsheet]
    pattern = input().strip()
    
    # Loop until valid pattern is chosen
    while pattern != '2':
        if pattern in ['1','3']:
            print("This feature is incomplete. Please try again.\n")
        else: 
            print("Input not recognized! Please try again.\n")
        pattern = input().strip()
    
    # Get list of carbon indices to functionalize
    if pattern == '2':
        while True:
            pct_input = input("Please specify a coverage percentage: ")
            try:
                cov_pct = float(pct_input)
                break 
            except ValueError:
                print("That's not a valid number. Please try again.")

        mod_indices = patternlist[int(pattern) - 1](coord_graph, cov_pct)
    else:
        mod_indices = patternlist[int(pattern) - 1](coord_graph)

    mod_coord_graph = copy.deepcopy(coord_graph)
    mod_coord_graph = attach_group(mod_coord_graph, grp, mod_indices)
    return mod_coord_graph
