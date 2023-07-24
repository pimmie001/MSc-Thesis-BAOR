import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *


def preparations_EEF(I):
    """Some preparations for the EEF"""

    I.A = [] # set of arcs
    for i in I.adj_list:
        for j in I.adj_list[i]:
            I.A.append((i,j))

    return 



def EEF2(I):
    """Solves the KEP using the Extended Edge Formulation (EEF)"""


    ### preparations
    preparations_EEF(I)
    L = I.n
    I.make_pred_list()


    ### create model
    m = gp.Model('KEP HCF')
    gp.setParam('LogFile', 'Logfiles/gurobi_hcf.log')
    m.ModelSense = GRB.MAXIMIZE


    ### variables
    vars = [[] for _ in range(L)]
    arc_to_index = {}

    for i,arc in enumerate(I.A):
        arc_to_index[arc] = i

        for l in range(L):
            x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x^{l}_{arc}')
            vars[l].append(x)


    ### constrains
    ## 7b
    for i in range(I.n):
        for l in range(L):
            left =[]
            right = []
            for j in I.pred_list[i]:
                left.append(vars[l][arc_to_index[(j,i)]])
            for j in I.adj_list[i]:
                right.append(vars[l][arc_to_index[(i,j)]])
            m.addConstr(sum(left) == sum(right))

    ## 7c
    for i in range(I.n):
        left = []
        for l in range(L):
            for j in I.adj_list[i]:
                left.append(vars[l][arc_to_index[(i,j)]])
        m.addConstr(sum(left) <= 1)

    ## 7d 
    for l in range(L):
        m.addConstr(sum(vars[l]) <= I.K)



    ### solve model
    m.write("EEF.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()

    ### make solution class
    solution = KEP_solution(I)
    solution.formulation = 'EEF'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.LB = m.ObjVal # best lower bound (= objective value current solution)
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    ### ! TODO:
    # solution.indices = [v.index for v in m.getVars() if v.x > 0.5] 

    return solution

