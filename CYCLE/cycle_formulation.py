import numpy as np
import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *



def get_cycles(I):
    """
    given an instance I, generatate all cycles of size K or less
    makes use of symmetry reduction
    """


    ### create floyd matrix
    floyd = np.full((I.n, I.n), I.n) # initialize matrix
    for i in I.adj_list: 
        for j in I.adj_list[i]:
            floyd[i,j] = 1 # set direct neighbors distance to 1

    for i in range(I.n):
        for j in range(I.n):
            for k in range(I.n):
                floyd[j,k] = min(floyd[j,k], floyd[j,i] + floyd[i,k])


    ### find cycles
    C = []

    for i in range(I.n): # i = starting node cycle
        curC = [[i]] # current cycle list
        for j in range(1, I.K+1): # j = length current cycle
            newC = [] # new cycle list
            for k in range(len(curC)): # k loops over current cycles (to extend them and possible add them to C)
                for l in range(len(I.adj_list[curC[k][-1]])): # l loops over neighbors
                    if I.adj_list[curC[k][-1]][l] >= i:
                        if I.adj_list[curC[k][-1]][l] == i: # add if cycle complete
                            C.append(curC[k][:])
                        else:                               # else continue exploring
                            if floyd[I.adj_list[curC[k][-1]][l],i] <= I.K - j:
                                add = True
                                for m in range(1, j):
                                    if curC[k][m] == I.adj_list[curC[k][-1]][l]:
                                        add = False
                                        break
                                if add:
                                    newC.append(curC[k][:])
                                    newC[-1].append(I.adj_list[curC[k][-1]][l])
            curC = newC

    return C



def cycle_formulation(I):
    """
    given an instance I, solves the KEP using the cycle formulation
    """


    C = get_cycles(I) # determine set of cycles
    I.C = C

    ### create model
    m = gp.Model(f'KEP cycle formulation {I.filename}')
    gp.setParam('LogFile', 'Logfiles/gurobi_cf.log')
    m.ModelSense = GRB.MAXIMIZE

    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraint later
    for i,c in enumerate(C):
        x = m.addVar(vtype = GRB.BINARY, obj = len(c), name = f'x_{i}')
        bin_vars.append(x)

    ### constraints
    expressions = [ [] for _ in range(I.n) ] # using expression list avoids having extra if statement: no "if node in c" is needed
    for i,c in enumerate(C):
        for node in c:
            expressions[node].append(bin_vars[i])
    for expression in expressions:
        if len(expression) > 1:
            m.addConstr(sum(expression) <= 1)

    ### solve model
    # m.write("model.lp")
    m.setParam('OutputFlag', False)
    m.optimize()

    ### make solution class
    solution = KEP_solution(I)
    solution.formulation = 'CF'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.LB = m.ObjVal # best lower bound (= objective value current solution)
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    ### determine chosen cycles (for ao feasibility check)
    solution.indices = [v.index for v in m.getVars() if v.x > 0.5]

    ### solve relaxation
    m_relax = m.relax()
    m_relax.optimize()
    solution.CUB = m_relax.ObjVal # continuous upper bound

    return solution

