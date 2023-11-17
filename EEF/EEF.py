import gurobipy as gp
from gurobipy import GRB
import time

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *
from EEF.min_eef import min_eef
from EEF.min_eef_heuristics import *



def floyd_matrix(I, l):
    """
    Returns floyd matrix when only considering nodes that are greater than or equal to l
    """

    floyd = np.full((I.n, I.n), I.n) # initialize matrix
    for i in range(l, I.n):
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



def EEF(I, method='REEF', get_variable_count=False):
    """
    Given instance I, solves the KEP using the Extended Edge Formulation (EEF)
    method: 
            REEF: EEF with all 3 variable reductions
                note: for d^l to be defined correctly for REEF, requires I.K <= I.n
            min: ILP model to find minimum number of variables
            heuristic: will find a heuristic solution for the minimum number activated variables

    Returns a solution containing information such as runtime (including time for preparations), number of variables etc. 
    If get_variable_count is true, will only return number of activated variables in EEF.
    """


    ### create model
    m = gp.Model('KEP REEF')
    m.ModelSense = GRB.MAXIMIZE
    m.setParam('OutputFlag', False)
    m.setParam('Threads', 1)
    m.setParam('MemLimit', 28)


    start_get_variable = time.time()
    if method == 'REEF': # ordered instance
        ### preparations
        I.preparations_EEF() # creates set of arcs I.A
        L = I.n # set L
        I.make_pred_list() # build predecessor list

        d = [floyd_matrix(I, l) for l in range(L)] # distance matrix for each copy l of the graph (d^l_(i,j)) #! takes long time
        V_l = [[i for i in range(l, I.n) if d[l][l,i] + d[l][i,l] <= I.K] for l in range(L)] # V^l
        L_fancy = [l for l in range(L) if len(V_l[l]) > 0]
        A_l = [[(i,j) for (i,j) in I.A if (i in V_l[l] and j in V_l[l] and d[l][l,i] + 1 + d[l][j,l] <= I.K)] for l in range(L)] # A^l

        end_get_variables = time.time() - start_get_variable

        start_build = time.time()

        ### variables and objective (9a)
        vars = []
        arc_to_index = {} # to find back variables for the constraints
        var_count = 0

        nvars = []
        for l in L_fancy:
            for (i,j) in A_l[l]:
                x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x^{l}_{i},{j}')
                vars.append(x)
                arc_to_index[(l,i,j)] = var_count
                var_count += 1
            nvars.append(len(A_l[l]))


        if get_variable_count:
            return var_count


        ### constrains
        union_V = set(element for subarray in V_l for element in subarray)

        ## expression lists
        arcs_in = [[[] for _ in range(I.n)] for _ in range(I.n)] # arcs going in (constraint 9b)
        arcs_out = [[[] for _ in range(I.n)] for _ in range(I.n)] # arcs going out (constraint 9b, 9e)
        arcs_out_tot = [[] for _ in range(len(union_V))] # arcs going out over all copies l (constraint 9c)
        max_size = [[] for _ in range(I.n)] # max cycle length (constraint 9d)
        arcs_out_l = [[] for _ in range(I.n)] # RHS only depends on l (constraint 9e)

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


    else: # unordered instance
        ### preparations
        if method == 'min':
            min_eef_solution = min_eef(I)
        elif method == 'heuristic':
            min_eef_solution = heuristic_eef(I)
        elif method == 'heuristic2':
            min_eef_solution = heuristic2_eef(I)

        end_get_variables = time.time() - start_get_variable

        start_build = time.time()

        ### variables and objective
        vars = []
        vars_arcs = []
        arc_to_index = {}
        var_count = 0

        nvars = []
        for l in range(I.n):
            var_count_l = 0
            for (i,j) in I.A:
                if min_eef_solution.yvalues[min_eef_solution.dict_y[(l,i,j)]] > 0.5:
                    x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x^{l}_{i},{j}')
                    vars.append(x)
                    vars_arcs.append((l,i,j))
                    arc_to_index[(l,i,j)] = var_count
                    var_count += 1
                    var_count_l += 1
            nvars.append(var_count_l)


        if get_variable_count:
            return var_count


        ## constraints (with expression lists)
        arcs_in = [[[] for _ in range(I.n)] for _ in range(I.n)] # arcs going in (constraint 9b)
        arcs_out = [[[] for _ in range(I.n)] for _ in range(I.n)] # arcs going out (constraint 9b, 9e)
        arcs_out_tot = [[] for _ in range(I.n)] # arcs going out over all copies l (constraint 9c)
        max_size = [[] for _ in range(I.n)] # max cycle length (constraint 9d)
        arcs_out_l = [[] for _ in range(I.n)] # RHS only depends on l (constraint 9e)

        ## add variables to expression lists
        for (l,i,j) in vars_arcs:
            x = vars[arc_to_index[(l,i,j)]] # x^l_ij

            arcs_in[l][j].append(x)
            arcs_out[l][i].append(x)
            arcs_out_tot[i].append(x)
            max_size[l].append(x)
            if i == l: arcs_out_l[l].append(x)

        ## add constraints to model
        for l in range(I.n):
            if max_size[l]: m.addConstr(sum(max_size[l]) <= I.K) # 9d
            for i in range(I.n):
                if arcs_in[l][i] or arcs_out[l][i]: m.addConstr(sum(arcs_in[l][i]) == sum(arcs_out[l][i])) # 9b
                if arcs_out[l][i] or arcs_out_l[l]: m.addConstr(sum(arcs_out[l][i]) <= sum(arcs_out_l[l])) # 9e

        for i in range(I.n):
            m.addConstr(sum(arcs_out_tot[i]) <= 1) # 9c


    ### end building model
    build_model = time.time() - start_build


    ### solve model
    # m.write(f"EEF.{method}.lp")
    m.optimize()


    ### return solution
    solution = KEP_solution(I)
    solution.formulation = 'EEF'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.obj = m.ObjVal
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.LB = m.ObjVal # best lower bound
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    ## to extract cycles and perform feasiblity check:
    solution.xvalues = [x.X for x in vars]
    solution.arc_to_index = arc_to_index

    ## for comparison
    solution.num_vars = m.NumVars
    solution.variance = np.var([x for x in nvars]) # variance of number of activated variables in graphs
    solution.get_variables = end_get_variables
    solution.time_build_model = build_model # building time
    solution.runtime = m.Runtime # solving time
    solution.total_time = build_model + m.Runtime # total time

    return solution

