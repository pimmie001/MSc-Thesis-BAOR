import numpy as np
import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from find_cycles import *



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
    I.C = []

    for i in range(I.n): # i = starting node cycle
        curC = [[i]] # current cycle list
        for j in range(1, I.K+1): # j = length current cycle
            newC = [] # new cycle list
            for k in range(len(curC)):
                for l in range(len(I.adj_list[curC[k][-1]])):
                    if I.adj_list[curC[k][-1]][l] >= i:
                        if I.adj_list[curC[k][-1]][l] == i: # add if cycle complete
                            I.C.append(curC[k][:])
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

    return



def cycle_formulation(I):
    """
    given an instance I, solves the KEP using the cycle formulation
    """


    get_cycles(I) # determine set of cycles

    ### create model
    m = gp.Model(f'KEP cycle formulation {I.filename}')

    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraint later
    for i,c in enumerate(I.C):
        x = m.addVar(vtype = GRB.BINARY, obj = len(c), name = f'x_{i}')
        bin_vars.append(x)


    # ! oude constraints
    # for node in I.nodes:
    #     active_variables = []
    #     for i,c in enumerate(C):
    #         if node in c:
    #             active_variables.append(bin_vars[i])
    #     if active_variables:
    #         m.addConstr(sum(active_variables) <= 1)


    ### constraints
    expressions = [ [] for _ in range(I.n) ] # using expression list avoids having extra if statement: no "if node in c" is needed
    for i,c in enumerate(I.C):
        for node in c:
            expressions[node].append(bin_vars[i])
    for expression in expressions:
        if expression:
            m.addConstr(sum(expression) <= 1)

    ### solve and show results
    m.ModelSense = GRB.MAXIMIZE
    m.write("model.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()


    # TODO: create/return solution 
    if m.status == gp.GRB.OPTIMAL: # Check if the model is optimized successfully
        objective_value = m.getAttr('ObjVal')
        return objective_value
    else:
        return -1


