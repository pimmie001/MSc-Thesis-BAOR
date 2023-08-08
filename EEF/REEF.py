import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *
from EEF.EEF import preparations_EEF



def REEF(I): #TODO!: finish
    """
    Solves the KEP using the Reduced Extended Edge Formulation (REEF):
    This is the original EEF with variable reductions.
    """


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
    m.write("REEF.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()


    ### make solution class
    solution = KEP_solution(I)
    solution.formulation = 'REEF'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.LB = m.ObjVal # best lower bound (= objective value current solution)
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    solution.xvalues = [[x.X for x in vars[l]] for l in range(L)]


    return solution

