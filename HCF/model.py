import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CYCLE.cycle_formulation import get_cycles


class min_hc_solution:
    """TODO"""

    def __init__(self, I):
        self.I = I # corresponding instance



def get_index_HC(hc, c2i, H_full):
    """
    First checks if hc has been created before. If not it will add the hc to the c2i (dict) and H_full (list)
    Secondly returns the index of the hc
    """

    if hc in c2i:
        return c2i[hc]

    index = len(c2i)
    c2i[hc] = index
    H_full.append(hc)
    return index


def model(I): # TODO: change name
    """
    ILP model to determine the minimum amount of half cycles needed to cover for all cycles
    First determines matrix M, containing indices of unique half cycles and create a list H_full that stores the halfcycles
    Secondly solves the ILP model

    For odd K, model requires a different ILP model than 'HCF.py' because there is no symmetry reduction to determine 
    the set of half-cycles and therefore it is possible that cycles of size (K+1) are created
    """


    ##### Preparations
    C = get_cycles(I)

    c2i = {} # (half)cycle to index to keep track of cycle indices
    H_full = [] # list with distinct halfcycles (used to retrieve actual cycle in solution)
    M = [] # list of dimensions len(c) * #hc_pairs * 2 that keeps track of indices of halfcycles; needed for the ILP formulation

    for cycle in C:
        M_sub = []

        if len(cycle) % 2 == 0: # even
            for i in range(len(cycle)//2):
                # make half cycles:
                hc1 = ()
                hc2 = ()
                for j in range(i, i + len(cycle)//2 + 1):
                    hc1 += (cycle[j%len(cycle)],)
                    hc2 += (cycle[(j+len(cycle)//2)%len(cycle)],)

                # store half_cycles and index:
                M_sub.append((get_index_HC(hc1, c2i, H_full), get_index_HC(hc2, c2i, H_full)))

        else: # odd
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
    index = 0 # for (1)
    i = 0 # for (2)

    for k in range(n_c):
        cycle = C[k]
        num_pairs = len(M[k]) # number of hc pairs

        # (1) at least one HC pair is chosen for every cycle:
        m.addConstr(sum([vars_y[ii] for ii in range(index, index+num_pairs)]) >= 1)
        index += num_pairs

        # (2) both halfcycle pairs (x) must be chosen if corresponding y is set to 1:
        for l in range(num_pairs): # choice combine or split constraints
            # # combine constraints
            # m.addConstr(vars_x[M[k][l][0]] + vars_x[M[k][l][1]] >= 2*vars_y[i])
        
            # split constraints (faster)
            m.addConstr(vars_x[M[k][l][0]] >= vars_y[i])
            m.addConstr(vars_x[M[k][l][1]] >= vars_y[i])

            i += 1


    ### solve model and show chosen half-cycles
    m.write("model choose hc.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()


    ### return solution
    solution = min_hc_solution(I)

    x_values = [x.X for x in vars_x]
    indices = [j for j, value in enumerate(x_values) if value > 0.5] # the indices of the chosen halfcycles

    # info on chosen halfcycles
    solution.xindices = indices
    solution.H_full = H_full
    solution.c2i = c2i

    # info on runtime/number vars etc. 
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs

    return solution

