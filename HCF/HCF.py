import numpy as np
import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *



def get_half_cycles(I):
    """
    Given an instance I, generatates all half-cycles of size (1 + ceil(K/2)) or less
    Uses symmetry reduction to reduce number of half cycles generated
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
                        break
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



def HCF(I):
    """
    given an instance I, solves the KEP using the half-cycle formulation
    """


    H = get_half_cycles(I) # determine set of half-cycles


    ### create model
    m = gp.Model('KEP half-cycle formulation')
    gp.setParam('LogFile', 'Logfiles/gurobi_hcf.log')
    m.ModelSense = GRB.MAXIMIZE


    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraints later
    for i,h in enumerate(H):
        x = m.addVar(vtype = GRB.BINARY, obj = len(h) - 1, name = f'x_{i}')
        bin_vars.append(x)


    ### constraints (numbers refer to constraint number in HCF paper)

    # create expressions lists
    expressions = [ [] for _ in range(I.n) ] # (5)
    expressions_half = [ [] for _ in range(I.n) ] # (5)
    left = [[[] for _ in range(I.n-i-1)] for i in range(I.n-1)] # (6)
    right = [[[] for _ in range(I.n-i-1)] for i in range(I.n-1)] # (6)
    constr_8 = I.K % 2 == 1 # (8) only needed if K odd
    M = (I.K+3)/2 # (8)

    for i,h in enumerate(H): # enumerating over H faster than looping over nodes
        # constraint (5):
        for j,node in enumerate(h):
            if j == 0 or j == len(h)-1: # start/end node count for halves only
                expressions_half[node].append(bin_vars[i])
            else:                       # middle nodes
                expressions[node].append(bin_vars[i])

        # constraint (6):
        start = h[0]
        end = h[-1]
        if start < end: # add to 'left' list
            left[start][end-start-1].append(bin_vars[i])
        else:           # add to 'right' list (start and end are swapped)
            right[end][start-end-1].append(bin_vars[i])

        # constraint (8):
        if constr_8:
            if len(h) == M and h[0] > h[-1]: # len(h) == M equivalent to |V^m(h)| == (K-1)/2
                m.addConstr(bin_vars[i] == 0)

    # add constraints to model
    for i in range(I.n):
        # constraint (5):
        expression = expressions[i]
        expression_half = expressions_half[i]
        if 0.5*len(expression_half) + len(expression) > 1:
            m.addConstr(0.5*sum(expression_half) + sum(expression) <= 1)

        # constraint (6):
        for j in range(I.n-i-1):
            if left[i][j] or right[i][j]:
                m.addConstr(sum(left[i][j]) == sum(right[i][j]))


    ### solve model
    m.write("model.lp")
    m.setParam('OutputFlag', False)
    m.optimize()

    ### show solution (progress)
    solution = KEP_solution(I)
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.LB = m.ObjVal # best lower bound (= objective value current solution)
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    # TODO: return cycles for feasiblity check 

    ### solve relaxation
    m_relax = m.relax()
    m_relax.setParam('OutputFlag', False)
    m_relax.optimize()
    solution.CUB = m_relax.ObjVal # continuous upper bound

    return solution

