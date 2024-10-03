import random as r
import math as m

__all__ = ['truerandsheet','pctrandsheet','restrandsheet','pctrandsandwich']

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

def pctrandsandwich(networkC,pct):
    # randomly selected carbons with user-specified percent coverage (for sandwich)
    prcarbons1 = []
    prcarbons2 = []
    print(networkC.number_of_nodes() / 2)
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