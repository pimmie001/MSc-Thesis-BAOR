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

