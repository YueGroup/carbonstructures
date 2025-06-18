import random as r
import math as m

__all__ = ['truerandsheet', 'pctrandsheet', 'restrandsheet', 'pctrandsandwich', 'truerandsandwich', 'restrandsandwich', 'pctrestrandsandwich']

def _findneighbors(graph,node):
    return list(graph.neighbors(node))

def truerandsheet(networkC):
    # truly random number and selection of carbons
    trcarbons = []
    pctcoverage = r.randint(0,100) / 100
    numC =  m.floor(pctcoverage * networkC.number_of_nodes())
    while len(trcarbons) < numC:
        index = r.randint(0,networkC.number_of_nodes() - 1)
        if index not in trcarbons:
            trcarbons.append(index)
    return trcarbons

def pctrandsheet(networkC,pct):
    # randomly selected carbons with user-specified percent coverage
    prcarbons = []
    pctcoverage = pct / 100
    numC =  m.floor(pctcoverage * networkC.number_of_nodes())
    while len(prcarbons) < numC:
        index = r.randint(0,networkC.number_of_nodes() - 1)
        if index not in prcarbons:
            prcarbons.append(index)
    return prcarbons

def restrandsheet(networkC):
    # randomly selected carbons with restricted coverage
    rrcarbons = []
    pctcoverage = r.randint(0,40) / 100
    numC =  m.floor(pctcoverage * networkC.number_of_nodes())
    while len(rrcarbons) < numC:
        index = r.randint(0,networkC.number_of_nodes() - 1)
        if set(rrcarbons).isdisjoint(set([index] + _findneighbors(networkC,index))):
            rrcarbons.append(index)
    return rrcarbons

def truerandsandwich(networkC):
    # truly random number and selection of carbons for each sheet
    trcarbons1 = []
    trcarbons2 = []
    pctcoverage = r.randint(0, 100) / 100
    numC = m.floor(pctcoverage * (networkC.number_of_nodes() / 2))

    while len(trcarbons1) < numC:
        index = r.randint(0, int(networkC.number_of_nodes() / 2) - 1)
        if index not in trcarbons1:
            trcarbons1.append(index)

    while len(trcarbons2) < numC:
        index = r.randint(int(networkC.number_of_nodes() / 2), networkC.number_of_nodes() - 1)
        if index not in trcarbons2:
            trcarbons2.append(index)

    return [trcarbons1, trcarbons2]

def pctrandsandwich(networkC,pct):
    # randomly selected carbons with user-specified percent coverage (for sandwich)
    prcarbons1 = []
    prcarbons2 = []
    # print(networkC.number_of_nodes() / 2)
    pctcoverage = pct / 100
    numC =  m.floor(pctcoverage * (networkC.number_of_nodes() / 2))
    while len(prcarbons1) < numC:
        index = r.randint(0,int(networkC.number_of_nodes() / 2) - 1)
        if index not in prcarbons1:
            prcarbons1.append(index)
    while len(prcarbons2) < numC:
        index = r.randint(int(networkC.number_of_nodes() / 2),networkC.number_of_nodes() - 1)
        if index not in prcarbons2:
            prcarbons2.append(index)
    return [prcarbons1, prcarbons2]

def restrandsandwich(networkC):
    # randomly selected carbons with restricted coverage for each sheet
    rrcarbons1 = []
    rrcarbons2 = []
    pctcoverage = r.randint(0, 40) / 100
    numC = m.floor(pctcoverage * (networkC.number_of_nodes() / 2))

    # Helper to find disjoint carbon selection
    def is_disjoint(selected, index, graph):
        neighbors = _findneighbors(graph, index)
        return set(selected).isdisjoint(set([index] + neighbors))

    # First sheet
    while len(rrcarbons1) < numC:
        index = r.randint(0, int(networkC.number_of_nodes() / 2) - 1)
        if is_disjoint(rrcarbons1, index, networkC):
            rrcarbons1.append(index)

    # Second sheet
    while len(rrcarbons2) < numC:
        index = r.randint(int(networkC.number_of_nodes() / 2), networkC.number_of_nodes() - 1)
        if is_disjoint(rrcarbons2, index, networkC):
            rrcarbons2.append(index)

    return [rrcarbons1, rrcarbons2]

def pctrestrandsandwich(networkC, pct):
    """
    Randomly select carbon atoms from both sheets of a graphene sandwich with:
      • user-defined percent coverage (pct), and
      • no neighboring atoms allowed (restricted).
    """
    rrcarbons1 = []
    rrcarbons2 = []
    pctcoverage = pct / 100
    numC = m.floor(pctcoverage * (networkC.number_of_nodes() / 2))

    def is_disjoint(selected, index, graph):
        neighbors = _findneighbors(graph, index)
        return set(selected).isdisjoint(set([index] + neighbors))

    # First sheet
    attempts = 0
    while len(rrcarbons1) < numC and attempts < 10 * numC:
        index = r.randint(0, int(networkC.number_of_nodes() / 2) - 1)
        # print(f"Trying index {index}, neighbors: {_findneighbors(networkC, index)}")
        if is_disjoint(rrcarbons1, index, networkC):
            rrcarbons1.append(index)
        attempts += 1

    if len(rrcarbons1) < numC:
        print(f"[Warning] Could only select {len(rrcarbons1)} out of {numC} target atoms for sheet 1 due to neighbor restrictions.")

    # Second sheet
    attempts = 0
    while len(rrcarbons2) < numC and attempts < 10 * numC:
        index = r.randint(int(networkC.number_of_nodes() / 2), networkC.number_of_nodes() - 1)
        if is_disjoint(rrcarbons2, index, networkC):
            rrcarbons2.append(index)
        attempts += 1

    if len(rrcarbons2) < numC:
        print(f"[Warning] Could only select {len(rrcarbons2)} out of {numC} target atoms for sheet 2 due to neighbor restrictions.")

    return [rrcarbons1, rrcarbons2]


