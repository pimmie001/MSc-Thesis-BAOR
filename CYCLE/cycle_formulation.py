import gurobipy as gp
from gurobipy import GRB
gp.setParam('LogFile', 'gurobi.log')

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from find_cycles import find_cycles



def cycle_formulation(arcs, nodes, K):
    C = find_cycles(arcs, nodes, K) # set of cycles of size <= K

    ### create model
    m = gp.Model('KEP cycle formulation')

    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraint later
    for i in range(len(C)):
        c = C[i]
        x = m.addVar(vtype = GRB.BINARY, obj = len(c), name = f'x_{i}')
        bin_vars.append(x)

    ### constraints
    for node in nodes:
        active_variables = []
        for i in range(len(C)):
            c = C[i]
            if node in c:
                active_variables.append(bin_vars[i])
        if active_variables:
            m.addConstr(sum(active_variables) <= 1)

    ### solve and show results
    m.ModelSense = GRB.MAXIMIZE
    # m.setParam( 'OutputFlag', False)
    m.optimize()

    if m.status == gp.GRB.OPTIMAL: # Check if the model is optimized successfully
        objective_value = m.getAttr('ObjVal')
        return objective_value
    else:
        return -1
