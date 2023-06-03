### Model to find min # of half-cycles
# TODO: test for small example

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CYCLE.cycle_formulation import *


def get_index_HC(hc, c2i, H_full):
    """
    First checks if hc has been created before. If so it will return its index and if not it will add the hc to the list i2c
    Secondly returns the index of the hc
    """

    if hc in c2i:
        return c2i[hc]

    index = len(c2i)
    c2i[hc] = index
    H_full.append(hc)
    return index


def model(I):
    # C = get_cycles(I) # !!!!
    C = [['A','B','C','D'],['A','B','C'], ['D','A','B','C']] #! test

    c2i = {} # (half)cycle to index to keep track of cycle indices
    H_full = [] # list with distinct halfcycles (used to retrieve actual cycle in solution)
    M = [] # list of dimensions len(c) * #hc * 2 that keeps track of indices of halfcycles; important for the ILP formulation


    for cycle in C:
        M_sub = []

        if len(cycle) % 2 == 0:
            for i in range(len(cycle)//2):
                # make half cycles:
                hc1 = ()
                hc2 = ()
                for j in range(i, i + len(cycle)//2 + 1):
                    hc1 += (cycle[j%len(cycle)],)
                    hc2 += (cycle[(j+len(cycle)//2)%len(cycle)],)

                # store half_cycles and index:
                M_sub.append((get_index_HC(hc1, c2i, H_full), get_index_HC(hc2, c2i, H_full)))

        else:
            for i in range(len(cycle)):
                # make half cycles:
                hc1 = ()
                hc2 = ()
                for j in range(i, i + len(cycle)//2 + 2):
                    hc1 += (cycle[j%len(cycle)],)
                    if j == i + len(cycle)//2 + 1: # hc2 has one element less than hc1
                        continue
                    hc2 += (cycle[(j+len(cycle)//2+1)%len(cycle)],)

                # store half_cycles and index:
                M_sub.append((get_index_HC(hc1, c2i, H_full), get_index_HC(hc2, c2i, H_full)))

        M.append(M_sub)

    # print(M)
    # print(H_full)
    # print(len(H_full))

# model(3)
