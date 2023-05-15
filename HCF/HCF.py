import gurobipy as gp
from gurobipy import GRB
from math import ceil

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from find_cycles import find_half_cycles



def HCF(arcs, nodes, K):
    M = 1 + ceil(K/2)
    H = find_half_cycles(arcs, nodes, M)

    ### create model
    m = gp.Model('KEP cycle formulation')


    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraint later
    for i in range(len(H)):
        h = H[i]
        x = m.addVar(vtype = GRB.BINARY, obj = len(h) - 1, name = f'x_{i}')
        bin_vars.append(x)


    ### constraints
    # constraint (5)
    for node in nodes:
        active_variables_half = [] # only count 0.5 in constraint (5) of HCF
        active_variables = []
        for i in range(len(H)):
            h = H[i]
            if node == h[0] or node == h[-1]:
                active_variables_half.append(bin_vars[i])
            elif node in h[1:-1]:
                active_variables.append(bin_vars[i])
        if active_variables_half or active_variables:
            m.addConstr(0.5 * sum(active_variables_half) + sum(active_variables) <= 1)

    # constraint (6)
    for i in range(len(nodes)):
        node1 = nodes[i]
        for j in range(i+1, len(nodes)):
            node2 = nodes[j]

            left = []
            right = []
            for k in range(len(H)):
                h = H[i]
                if node1 == h[0] and node2 == h[-1]:
                    left.append(bin_vars[k])
                if node1 == h[-1] and node2 == h[0]:
                    right.append(bin_vars[k])

            if left or right:
                m.addConstr(sum(left) == sum(right))

    # constraint (8)
    if K % 2 == 1: # only for odd K
        for i in range(len(H)):
            h = H[i]
            if h[0] > h[-1] and len(h)-2 == (K-1)/2: ### TODO: NEED NODE ORDER
                m.addConstr(bin_vars[i] == 0)


    ### solve and show results
    m.ModelSense = GRB.MAXIMIZE
    m.setParam( 'OutputFlag', False)
    m.optimize()

    if m.status == gp.GRB.OPTIMAL: # Check if the model is optimized successfully
        objective_value = m.getAttr('ObjVal')
        return objective_value
    else:
        return -1
