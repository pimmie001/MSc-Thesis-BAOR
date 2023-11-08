import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CYCLE.CF import get_cycles



class min_eef_solution:
    """Simple class for min_eef solution"""

    def __init__(self, I):
        self.I = I # corresponding instance



def arcs_in_cycle(c):
    # given cycle [1,2,3] returns the arcs in the cycle [(1,2), (2,3), (3,1)]
    arcs = []
    for i in range(len(c)-1):
        arcs.append((c[i],c[i+1]))
    arcs.append((c[-1],c[0]))
    return arcs



def min_eef(I, time_limit=None):
    """
    ILP model to determine the minimum number of variables to be activated in the (reduced) EEF model.
    """


    ### preparations
    I.preparations_EEF() # create set of arcs
    C = get_cycles(I) # create set of cycles
    if time_limit is None:
        time_limit = 600


    ### create model
    m = gp.Model('min EEF ILP')
    m.ModelSense = GRB.MINIMIZE


    ### create variables
    # y^l_ij = 1 iff variable x^l_ij is activated
    yvars = []
    dict_y = {} # to find back the variables
    varcount = 0
    for l in range(I.n):
        for (i,j) in I.A:
            y = m.addVar(vtype=GRB.BINARY, obj = 1, name = f'y^{l}_{i},{j}')
            yvars.append(y)
            dict_y[(l,i,j)] = varcount
            varcount += 1

    # z^l_k = 1 iff cycle k can be made in copy l
    zvars = []
    dict_z = {}
    varcount = 0
    for l in range(I.n):
        for k in range(len(C)):
            z = m.addVar(vtype=GRB.BINARY, obj = 0, name = f'z^{l}_{k}')
            zvars.append(z)
            dict_z[(l,k)] = varcount
            varcount += 1


    ### constraints
    # (1) all cycles must be made in at least one copy
    for k in range(len(C)):
        LHS = []
        for l in C[k]:
            LHS.append(zvars[dict_z[(l,k)]])
        m.addConstr(sum(LHS) >= 1)


    # (2) y^l_ij = 1 for all (i,j) in C_k, for all l, k such that z^l_k = 1
    for k in range(len(C)):
        for l in range(I.n):
            for (i,j) in arcs_in_cycle(C[k]):
                m.addConstr(yvars[dict_y[(l,i,j)]] >= zvars[dict_z[(l,k)]])

    # # alternative for constraint (2)   (is slower)
    # for k in range(len(C)):
    #     for l in range(I.n):
    #         m.addConstr(sum([yvars[dict_y[(l,i,j)]] for (i,j) in arcs_in_cycle(C[k])]) >= len(C[k]) * zvars[dict_z[(l,k)]])



    ### solve model
    # m.write("min_eef.lp")
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', time_limit)
    m.optimize()


    ### return solution
    solution = min_eef_solution(I)

    solution.optimality = m.Status == GRB.OPTIMAL
    solution.obj = m.ObjVal
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs

    # to extract cycles and perform feasiblity check:
    solution.yvalues = [x.X for x in yvars]
    solution.zvalues = [x.X for x in zvars]
    solution.dict_y = dict_y
    solution.dict_z = dict_z

    return solution

