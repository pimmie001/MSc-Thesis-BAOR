import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *



def find_all_paths(I):
    # Finds all paths of length K (hence K+1 nodes) for the given instance

    all_paths = []
    for start in range(I.n):
        paths_cur = [[start]] # current list of paths

        for _ in range(I.K): # add a neighbor K times to get path of length K
            paths_copy = paths_cur.copy() # create copy
            paths_cur = [] # reset current paths 

            for path in paths_copy: # loop over copy
                last = path[-1]
                for neighbor in I.adj_list[last]:
                    if neighbor not in path:
                        new_path = path + [neighbor]
                        paths_cur.append(new_path) # append current paths with neighbor added

        all_paths.extend(paths_cur)

    return all_paths



def EF(I):
    """
    given an instance I, solves the KEP using the edge formulation (EF)
    """

    ### preparations
    I.preparations_EEF()
    I.make_pred_list() 
    paths = find_all_paths(I) # determine paths of length K


    ### create model
    m = gp.Model(f'KEP edge formulation {I.filename}')
    m.ModelSense = GRB.MAXIMIZE


    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraint later
    x_dict = {}
    varcount = 0
    for (i,j) in I.A:
        x = m.addVar(vtype = GRB.BINARY, obj = 1, name = f'x_{i},{j}')
        bin_vars.append(x)
        x_dict[(i,j)] = varcount
        varcount += 1


    ### constraints
    for i in range(I.n):
        ## flow conservation
        flow_in = []
        for j in I.pred_list[i]:
            flow_in.append(bin_vars[x_dict[(j,i)]])

        flow_out = []
        for j in I.adj_list[i]:
            flow_out.append(bin_vars[x_dict[(i,j)]])

        m.addConstr(sum(flow_in) == sum(flow_out), name = f'flow_{i}')

        ## each node selected in at most one cycle
        m.addConstr(sum(flow_out) <= 1)

    ## path constraints to ensure cycles of size <= K
    for path in paths:
        arcs_in_path = []
        for i in range(I.K):
            arcs_in_path.append((path[i],path[i+1]))

        vars_in_path = []
        for (i,j) in arcs_in_path:
            vars_in_path.append(bin_vars[x_dict[(i,j)]])

        m.addConstr(sum(vars_in_path) <= I.K - 1)


    ### solve model
    m.setParam('OutputFlag', False)
    # m.write('EF.lp')
    m.optimize()

    ### return solution
    solution = KEP_solution(I)
    solution.formulation = 'EF'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.obj = m.ObjVal

    # get selected edges
    if solution.optimality:
        solution.edges = []
        values = m.getAttr('x', bin_vars)
        for (i,j), ind in x_dict.items():
            val = values[ind]
            if val > 0.5:
                solution.edges.append((i,j))

    return solution
