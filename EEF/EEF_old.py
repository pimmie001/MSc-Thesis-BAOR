import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *



def preparations_EEF(I):
    """Some preparations for the EEF"""

    I.L = I.K // 2 # upperbound on the number of cycles

    I.A = [] # set of arcs
    for i in I.adj_list:
        for j in I.adj_list[i]:
            I.A.append((i,j))

    return 



def EEF(I):
    """Solves the KEP using the Extended Edge Formulation (EEF)"""  


    ### preparations
    preparations_EEF(I)


    ### create model
    m = gp.Model(f'KEP EEF: {I.filename}')
    gp.setParam('LogFile', 'Logfiles/gurobi_eef.log')
    m.ModelSense = GRB.MAXIMIZE


    ### variables
    vars = [[] for _ in range(I.L)] # Create a list to store the binary variables to use them in constraints later
    arc2ind = {} # to find index of the arcs
    ind = 0
    for arc in I.A:
        arc2ind[arc] = ind
        ind += 1
        for l in range(I.L):
            x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x_{arc}^{l}')
            vars[l].append(x)


    ### constraints
    # ! use cycle formulation to add constraints: see if infeasible ?

    # ## expression lists # TODO: simplify
    # list1_L = [[[] for _ in range(I.L)] for _ in range(I.n)]
    # list1_R = [[[] for _ in range(I.L)] for _ in range(I.n)]
    # list2 = [[] for _ in range(I.n)]
    # list3 = [[] for _ in range(I.L)]

    # for l in range(I.L):
    #     for i in range(I.n):
    #         for j in range(I.n):
    #             if I.adj_matrix[i,j]:
    #                 list1_R[i][l].append(vars[l][arc2ind[(i,j)]])
    #                 list2[i].append(vars[l][arc2ind[(i,j)]])
    #                 list3[l].append(vars[l][arc2ind[(i,j)]])

    #             if I.adj_matrix[j,i]:
    #                 list1_L[i][l].append(vars[l][arc2ind[(j,i)]])

    # ## add to model
    # for i in range(I.n):
    #     for l in range(I.L):
    #         m.addConstr(sum(list1_L[i][l]) == sum(list1_R[i][l]))

    #     m.addConstr(sum(list2[i]) <= 1)

    # for l in range(I.L):
    #     m.addConstr(sum(list3[l]) <= I.K)



    for i in range(I.n):
        for l in range(I.L):
            left = []
            right = []
            for j in range(I.n):
                if I.adj_matrix[i,j]:
                    right.append(vars[l][arc2ind[(i,j)]])
                if I.adj_matrix[j,i]:
                    left.append(vars[l][arc2ind[(j,i)]])
            m.addConstr(sum(left) == sum(right))

    for i in range(I.n):
        LHS = []
        for j in range(I.n):
            if I.adj_matrix[i,j]:
                for l in range(I.L):
                    LHS.append(vars[l][arc2ind[(i,j)]])
        m.addConstr(sum(LHS) <= 1)

    for l in range(I.L):
        LHS = []
        for i in range(I.n):
            for j in I.adj_list[i]:
                LHS.append(vars[l][arc2ind[(i,j)]])
        m.addConstr(sum(LHS) <= I.K)



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

