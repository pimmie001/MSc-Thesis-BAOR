import numpy as np
import gurobipy as gp
from gurobipy import GRB
gp.setParam('LogFile', 'gurobi_hcf.log')

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *


# TODO: test
# TODO: test with different node orders
def get_half_cycles(I):
    """
    given an instance I, generatate all half-cycles of size (1 + ceil(K/2)) or less
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


    ### find half-cycles
    khcycles = [[[[] for _ in range(I.K)] for _ in range(I.n)] for _ in range(I.n)]
    for i in range(I.n): # starting node of cycles
        curC = [[i]] # current cycle list
        for j in range(1, (I.K+1)//2 + 1): # length cycle
            newC = [] # new cycle list
            for k in range(len(curC)): # loops over current cycles (to extend them and possible add them to C)
                for l in range(len(I.adj_list[curC[k][-1]])): # neighbors of last node in current cycle
                    # determine if a new cycle should be added to curC (and do so if true):
                    if I.adj_list[curC[k][-1]][l] != i and floyd[I.adj_list[curC[k][-1]][l]][i] <= I.K - j:
                        add = True
                        for m in range(1, j):
                            if curC[k][m] == I.adj_list[curC[k][-1]][l]:
                                add = False
                                break
                        if add:
                            newC.append(curC[k][:])
                            newC[-1].append(I.adj_list[curC[k][-1]][l])

            for k in range(len(newC)):
                add = True
                for l in range(1, len(newC[k]) - 1):
                    if newC[k][l] < newC[k][0] and newC[k][l] < newC[k][-1]:
                        add = False
                if add and (I.K % 2 == 0 or j < (I.K+1)//2 or newC[k][0] < newC[k][-1]):
                    khcycles[newC[k][0]][newC[k][-1]][len(newC[k])-1].append(newC[k])
            curC = newC

    hcycles = []
    for i in range(I.n):
        for j in range(i+1, I.n):
            for k in range(1, I.K):
                if len(khcycles[i][j][k]) > 0 and len(khcycles[j][i][k]) + len(khcycles[j][i][k-1]) > 0:
                    for l in range(len(khcycles[i][j][k])):
                        hcycles.append(khcycles[i][j][k][l])
                    for l in range(len(khcycles[j][i][k])):
                        hcycles.append(khcycles[j][i][k][l])
                    if len(khcycles[i][j][k-1]) == 0:
                        for l in range(len(khcycles[j][i][k-1])):
                            hcycles.append(khcycles[j][i][k-1][l])

    return hcycles


# ! untested
def HCF(I):
    """
    given an instance I, solves the KEP using the half-cycle formulation
    """


    H = get_half_cycles(I) # determine set of half-cycles
    print('cycles done')


    ### create model
    m = gp.Model('KEP half-cycle formulation')
    m.ModelSense = GRB.MAXIMIZE


    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraints later
    for i,h in enumerate(H):
        x = m.addVar(vtype = GRB.BINARY, obj = len(h) - 1, name = f'x_{i}')
        bin_vars.append(x)


    ### constraints (numbers refer to constraint number in HCF paper)

    # constraint (5)
    expressions = [ [] for _ in range(I.n) ]
    expressions_half = [ [] for _ in range(I.n) ]
    for i,h in enumerate(H):
        for j,node in enumerate(h):
            if j == 0 or j == len(h)-1: # start/end node count for halves only
                expressions_half[node].append(bin_vars[i])
            else: # middle nodes
                expressions[node].append(bin_vars[i])

    for k in range(I.n):
        expression = expressions[k]
        expression_half = expressions_half[k]
        if expression or expression_half:
        # TODO: test if len(expression) + 0.5*len(expression_half) > 1:
            m.addConstr(0.5*sum(expression_half) + sum(expression) <= 1)

    # # constraint (5) # ! old without expressions
    # for node in I.nodes:
    #     active_variables_half = [] # only count for 0.5
    #     active_variables = []
    #     for i in range(len(H)):
    #         h = H[i]
    #         if node == h[0] or node == h[-1]:
    #             active_variables_half.append(bin_vars[i])
    #         elif node in h[1:-1]:
    #             active_variables.append(bin_vars[i])
    #     if active_variables_half or active_variables:
    #         m.addConstr(0.5 * sum(active_variables_half) + sum(active_variables) <= 1)

    print('constraint 5')

    # constraint (6) #! new version with expression lists (not tested!!!!)
    left = [[[] for _ in range(I.n-i-1)] for i in range(I.n-1)]
    right = [[[] for _ in range(I.n-i-1)] for i in range(I.n-1)]
    for i,h in enumerate(H):
        start = h[0]
        end = h[-1]
        if start < end: # add to 'left' list
            left[start][end-start-1].append(bin_vars[i])
        else: # add to 'right' list (start and end are swapped)
            right[end][start-end-1].append(bin_vars[i])

    for i in range(I.n-1):
        for j in range(I.n-i-1):
            left_ij = left[i][j]
            right_ij = right[i][j]
            if left_ij or right_ij:
                m.addConstr(sum(left_ij) == sum(right_ij))


    # # constraint (6) # ! old version (SLOW) !!! 
    # for i, node1 in enumerate(I.nodes):
    #     for j in range(i+1, I.n):
    #         node2 = I.nodes[j]

    #         left = []
    #         right = []
    #         for k,h in enumerate(H):
    #             if node1 == h[0] and node2 == h[-1]:
    #                 left.append(bin_vars[k])
    #             if node1 == h[-1] and node2 == h[0]:
    #                 right.append(bin_vars[k])

    #         if left or right:
    #             m.addConstr(sum(left) == sum(right))

    print('constraint 6')

    # constraint (7): binary constraint already in variable definition

    # constraint (8)
    if I.K % 2 == 1: # only for odd K
        M = (I.K+3)/2
        for i,h in enumerate(H):
            if len(h) == M and h[0] > h[-1]: # len(h) == M equivalent to |V^m(h)| == (K-1)/2
                m.addConstr(bin_vars[i] == 0)
        print('constraint 8')


    ### solve model
    m.write("model.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()

    ### show solution (progress)
    solution = KEP_solution(I)
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.LB = m.ObjVal # best lower bound (= objective value current solution)
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    ### solve relaxation
    m_relax = m.relax()
    m_relax.setParam('OutputFlag', False)
    m_relax.optimize()
    solution.CUB = m_relax.ObjVal # continuous upper bound

    return solution

