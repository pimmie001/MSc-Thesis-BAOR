import gurobipy as gp
from gurobipy import GRB
import time

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



def REEF2(I):
    """
    Solves the KEP using the Reduced Extended Edge Formulation (REEF):
    REEF is the EEF with all 3 variable reductions.
    Uses expression lists
    For d^l to be defined correctly, requires I.K <= I.n
    """


    start_build = time.time()

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
    union_V = set(element for subarray in V_l for element in subarray)

    ## expression lists
    arcs_in = [[[] for _ in range(I.n)] for _ in range(I.n)] # arcs going in (constraint 9b)
    arcs_out = [[[] for _ in range(I.n)] for _ in range(I.n)] # arcs going out (constraint 9b, 9e)
    arcs_out_tot = [[] for _ in range(len(union_V))] # arcs going out over all copies l (constraint 9c)
    max_size = [[] for _ in range(I.n)] # max cycle length (constraint 9d)
    arcs_out_l = [[] for _ in range(I.n)] # RHS only depends on l (constraint 9)

    ## add variables to expression lists
    for l in L_fancy:
        for (i,j) in A_l[l]:
            x = vars[arc_to_index[(l,i,j)]] # x^l_ij

            arcs_in[l][j].append(x)
            arcs_out[l][i].append(x)
            arcs_out_tot[i].append(x)
            max_size[l].append(x)
            if i == l: arcs_out_l[l].append(x)

    ## add constraints to model
    for l in L_fancy:
        m.addConstr(sum(max_size[l]) <= I.K) # 9d
        for i in V_l[l]:
            m.addConstr(sum(arcs_in[l][i]) == sum(arcs_out[l][i])) # 9b
            m.addConstr(sum(arcs_out[l][i]) <= sum(arcs_out_l[l])) # 9e

    for i in union_V:
        m.addConstr(sum(arcs_out_tot[i]) <= 1) # 9c


    build_model = time.time() - start_build


    ### solve model
    m.write("REEF2.lp")
    m.setParam('OutputFlag', False)
    m.optimize()


    ### return solution
    solution = KEP_solution(I)
    solution.formulation = 'REEF'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.obj = m.ObjVal
    solution.time_build_model = build_model
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
