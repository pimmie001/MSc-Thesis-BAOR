### Model to find min # of half-cycles

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CYCLE.cycle_formulation import *


def get_index_HC(hc, c2i, H_full):
    """
    Checks if hc has been created before. If so it will return its index.
    If not, it will add the hc to the list i2c"""

    if hc in c2i:
        return c2i[hc]

    index = len(c2i)
    c2i[hc] = index
    H_full.append(hc)
    return index


def model(I):
    # C = get_cycles(I) # !!!!
    C = [['A','B','C','D'],['A','B','C'], ['A','D','C','B']] #! test

    c2i = {} # halfcycles to index
    H_full = [] # list with distinct halfcycles (used to retrieve actual cycle in solution)
    M = np.zeros((len(C),2)) # matrix with indices of the 2 half cycles corresponding to each cycle

    for cycle in C:
        if len(cycle) % 2 == 0:
            for i in range(len(cycle)//2):
                # make half cycles:
                hc1 = ()
                hc2 = ()
                for j in range(i, i + len(cycle)//2 + 1):
                    hc1 += (cycle[j%len(cycle)],)
                    hc2 += (cycle[(j+len(cycle)//2)%len(cycle)],)

                # store half_cycles and index:
                M[i,0] = get_index_HC(hc1, c2i, H_full)
                M[i,1] = get_index_HC(hc2, c2i, H_full)

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
                M[i,0] = get_index_HC(hc1, c2i, H_full)
                M[i,1] = get_index_HC(hc2, c2i, H_full)

#     print(H_full)
#     print(len(H_full))

# model(3)
