import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *
from EEF.EEF import preparations_EEF



def floyd_matrix(I, l):
    """
    Returns floyd matrix when only considering nodes that are greater than or equal to l
    """

    floyd = np.full((I.n, I.n), I.n) # initialize matrix
    for i in I.adj_list:
        if i >= l:
            floyd[i,i] = 0
            for j in I.adj_list[i]:
                if j >= l:
                    floyd[i,j] = 1 # set direct neighbors distance to 1

    # recursive loop:
    for i in range(l, I.n):
        for j in range(l, I.n):
            for k in range(l, I.n):
                floyd[j,k] = min(floyd[j,k], floyd[j,i] + floyd[i,k])

    return floyd



def REEF(I):
    """
    Solves the KEP using the Reduced Extended Edge Formulation (REEF):
    REEF is the EEF with all 3 variable reductions.
    For d^l to be defined correctly, requires I.K <= I.n
    """


    ### preparations
    preparations_EEF(I) # creates set of arcs I.A
    L = I.n # set L
    I.make_pred_list() # build predecessor list

    d = [floyd_matrix(I, l) for l in range(L)] # distance matrix for each copy l of the graph (d^l_(i,j))
    V_l = [[i for i in range(l, I.n) if d[l][l,i] + d[l][i,l] <= I.K] for l in range(L)] # V^l
    L_fancy = [l for l in range(L) if len(V_l[l]) > 0]
    A_l = [[(i,j) for (i,j) in I.A if (i in V_l[l] and j in V_l[l] and d[l][l,i] + 1 + d[l][j,l] <= I.K)] for l in range(L)] # A^l


    ### create model
    m = gp.Model('KEP REEF')
    m.ModelSense = GRB.MAXIMIZE
    # gp.setParam('LogFile', 'Logfiles/gurobi_reef.log')


    ### variables and objective (9a)
    vars = []
    arc_to_index = {} # to find back variables for the constraints
    var_count = 0

    for l in L_fancy:
        for (i,j) in A_l[l]:
            x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x^{l}_{i},{j}')
            vars.append(x)
            arc_to_index[(l,i,j)] = var_count
            var_count += 1


    ### constrains
    ## 9b
    for l in L_fancy:
        for i in V_l[l]:
            left = []
            right = []

            for j in I.pred_list[i]:
                if (j,i) in A_l[l]:
                    left.append(vars[arc_to_index[(l,j,i)]])

            for j in I.adj_list[i]:
                if (i,j) in A_l[l]:
                    right.append(vars[arc_to_index[(l,i,j)]])

            m.addConstr(sum(left) == sum(right))


    ## 9c
    union_V = set(element for subarray in V_l for element in subarray)
    for i in union_V:
        left = []
        for l in L_fancy:
            for j in I.adj_list[i]:
                if (i,j) in A_l[l]:
                    left.append(vars[arc_to_index[(l,i,j)]])

        m.addConstr(sum(left) <= 1)


    ## 9d
    for l in L_fancy:
        left = []
        for (i,j) in A_l[l]:
            left.append(vars[arc_to_index[(l,i,j)]])

        m.addConstr(sum(left) <= I.K)


    ## 9e
    for l in L_fancy:
        for i in V_l[l]:
            left = []
            right = []

            for j in I.adj_list[i]:
                if (i,j) in A_l[l]:
                    left.append(vars[arc_to_index[(l,i,j)]])

            for j in I.adj_list[l]:
                if (l,j) in A_l[l]:
                    right.append(vars[arc_to_index[(l,l,j)]])

            m.addConstr(sum(left) <= sum(right))



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

    # to extract cycles and perform feasiblity check:
    solution.xvalues = [x.X for x in vars]
    solution.arc_to_index = arc_to_index

    return solution

