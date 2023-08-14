import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from CYCLE.CF import get_cycles
from EEF.EEF import preparations_EEF



class min_eef_solution:
    """Simple class for min_eef solution"""

    def __init__(self, I):
        self.I = I # corresponding instance



def min_eef(I, time_limit=None):
    """TODO"""


    ### preparations
    preparations_EEF(I) # create set of arcs
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
    for l in range(len(I.n)):
        for (i,j) in I.A:
            y = m.addVar(vtype=GRB.BINARY, obj = 1)
            yvars.append(y)
            dict_y[(l,i,j)] = varcount
            varcount += 1

    # z^l_k = 1 iff cycle k can be made in copy l
    zvars = []
    dict_z = {}
    varcount = 0
    for l in range(len(I.n)):
        for k in range(len(C)):
            z = m.addVar(vtype=GRB.BINARY, obj = 0)
            zvars.append(z)
            dict_z[(l,k)] = varcount
            varcount += 1


    ### consraints
    # (1) all cycles must be made in at least one copy
    for k in range(len(C)):
        LHS = []
        for l in range(I.n):
            LHS.append(zvars[dict_z[(l,k)]])
        m.addConstr(sum(LHS) >= 1)

    # (2) y^l_ij = 1 for all (i,j) in C_k, l, k such that z^l_k = 1
    for k in range(len(C)):
        for l in range(len(I.n)):
            for (i,j) in C[k]:
                m.addConstr(yvars[dict_y[(l,i,j)]] >= zvars[dict_z[(l,k)]])


    ### solve model
    m.write("min_eef.lp")
    m.setParam('OutputFlag', False)
    m.setParam('TimeLimit', time_limit)
    m.optimize()


    ### return solution
    solution = min_eef_solution(I)

    # to extract cycles and perform feasiblity check:
    solution.yvalues = [x.X for x in yvars]
    solution.zvalues = [x.X for x in zvars]
    solution.dict_y = dict_y
    solution.dict_z = dict_z
    solution.obj = m.ObjVal
    print(solution.yvalues)
    print(solution.obj)

