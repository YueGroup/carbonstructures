import random as r
import math as m
import sys

__all__ = ['truerand','pctrand','restrand']

def _checkfloat(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def _enterpct():
    print("What percent coverage would you like?\n")
    pctinput = input()
    while True:
        if _checkfloat(pctinput):
            pct = float(pctinput)
            if 0 <= pct <= 100:
                return pct
            else:
                print("Invalid percentage! Please enter a number between 0 and 100. ")
        elif pctinput == 'exit()':
            sys.exit()
        else:
            print("Please enter a valid number. ")
        pctinput = input()

def _findneighbors(graph,node):
    return list(graph.neighbors(node))

def truerand(networkC):
    # truly random number and selection of carbons
    trcarbons = []
    pctcoverage = r.randint(0,100) / 100
    numC =  m.floor(pctcoverage * networkC.number_of_nodes())
    while len(trcarbons) < numC:
        index = r.randint(0,networkC.number_of_nodes() - 1)
        if index not in trcarbons:
            trcarbons.append(index)
    return trcarbons

def pctrand(networkC):
    # randomly selected carbons with user-specified percent coverage

    pct = _enterpct()

    prcarbons = []
    pctcoverage = pct / 100
    numC =  m.floor(pctcoverage * networkC.number_of_nodes())
    while len(prcarbons) < numC:
        index = r.randint(0,networkC.number_of_nodes() - 1)
        if index not in prcarbons:
            prcarbons.append(index)
    return prcarbons

def restrand(networkC):
    rrcarbons = []
    pctcoverage = r.randint(0,40) / 100
    numC =  m.floor(pctcoverage * networkC.number_of_nodes())
    while len(rrcarbons) < numC:
        index = r.randint(0,networkC.number_of_nodes() - 1)
        if set(rrcarbons).isdisjoint(set([index] + _findneighbors(networkC,index))):
            rrcarbons.append(index)
    return rrcarbons