import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from EEF.min_eef import *
from CYCLE.CF import get_cycles



def heuristic_eef(I):
    """Heuristic solution for finding minimum number of activated variables in the EEF"""

    # preparations
    C = get_cycles(I)
    I.preparations_EEF()

    # define variables 
    Y = dict()
    Z = dict()
    for l in range(I.n):
        for (i,j) in I.A:
            Y[(l,i,j)] = 0
        for k in range(len(C)):
            Z[(l,k)] = 0

    # main loop
    added = set()
    while len(added) < len(C): # all cycles need to be able to be made
        break
    return
