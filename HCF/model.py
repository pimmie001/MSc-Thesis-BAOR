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
    """
    ILP model to determine the minimum amount of half cycles needed to cover for all cycles
    First determines matrix M, containing indices of unique half cycles and create a list H_full that stores the halfcycles
    Secondly solves the ILP model
    """


    ##### Preparations
    C = get_cycles(I)
    # C = [['A','B','C','D'],['A','B','C'], ['D','A','B','C']] #! test

    c2i = {} # (half)cycle to index to keep track of cycle indices
    H_full = [] # list with distinct halfcycles (used to retrieve actual cycle in solution)
    M = [] # list of dimensions len(c) * #hc_pairs * 2 that keeps track of indices of halfcycles; needed for the ILP formulation


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



    ##### The ILP model
    m = gp.Model('Choose halfcycles ILP model')
    gp.setParam('LogFile', 'Logfiles/gurobi_choose_hc.log')


    n_c = len(C) # number of cycles
    n_h = len(H_full) # number of halfcycles
    n_p = sum([len(M[i]) for i in range(len(M))]) # number of HC pairs


    ### variables
    vars_x = [] # store x variables: 1 iff this half cycle is chosen
    vars_y = [] # store y variables: 1 iff this pair of halfcycles is chosen

    for j in range(n_h):
        x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x_{j}')
        vars_x.append(x)

    for i in range(n_p):
        y = m.addVar(vtype = GRB.BINARY, obj = 0, name = f'y_{i}')
        vars_y.append(y)


    ### constraints
    # at least one HC pair is chosen for every cycle
    count = 0
    for k in range(n_c):
        cycle = C[k]

        # determine set X_k and keep track of count:
        car_X_k = len(cycle)//2 if len(cycle)%2 == 0 else len(cycle) # cardinality of X_k: depends on length cycle and whether this length is odd or even
        X_k = range(count, count + car_X_k) # set X_k
        count += car_X_k
        print(X_k)

        LHS = []
        for i in X_k:
            LHS.append(vars_y[i])
        m.addConstr(sum(LHS) >= 1)

    # both halfcycle pairs (x) must be chosen if corresponding y is set to 1
    i = 0
    for k in range(n_c):
        for l in range(len(M[k])):
            m.addConstr(vars_x[M[k][l][0]] + vars_x[M[k][l][1]] >= 2*vars_y[i])
            i += 1


    ### solve model
    m.write("model choose hc.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()

