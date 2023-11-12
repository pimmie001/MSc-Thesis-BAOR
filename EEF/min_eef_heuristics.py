import sys, os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from EEF.min_eef import *
from CYCLE.CF import get_cycles



def arcs_in_cycle(c):
    # given cycle (eg [1,2,3]) returns the arcs in the cycle (eg [(1,2), (2,3), (3,1)])
    arcs = []
    for i in range(len(c)-1):
        arcs.append((c[i],c[i+1]))
    arcs.append((c[-1],c[0]))
    return arcs


def count_nodes(n, C, exclude):
    # count how often nodes occur in cycles that are not in exclude
    count = np.zeros(n)
    for i,cycle in enumerate(C):
        if i in exclude:
            continue
        for node in cycle:
            count[node] += 1
    return count



def heuristic_eef(I):
    """Heuristic solution for finding minimum number of activated variables in the EEF"""

    ### preparations
    C = get_cycles(I)
    I.preparations_EEF()


    ### define variables 
    Y = dict()
    Z = dict()
    for l in range(I.n):
        for (i,j) in I.A:
            Y[(l,i,j)] = 0
        for k in range(len(C)):
            Z[(l,k)] = 0


    ### main loop
    added = set()
    l = 0 # number of copy
    while len(added) < len(C): # all cycles need to be able to be made
        ## find most common node left
        count = count_nodes(I.n, C, added) # count occurences of nodes
        j = np.argmax(count)


        ## find which cycles include this node
        C_i = []
        for i,cycle in enumerate(C):
            if i in added:
                continue
            if j in cycle:
                added.add(i)
                C_i.append(cycle)
                Z[(l,i)] = 1

        ## activate variables corresponding to cycle
        for cycle in C_i:
            print(cycle)
            for (i,j) in arcs_in_cycle(cycle):
                print(i,j)
                Y[(l,i,j)] = 1
            print('\n')

        l += 1


    ### return solution
    solution = min_eef_solution(I)

    solution.dict_y = {}
    solution.dict_z = {}
    solution.yvalues = []
    solution.zvalues = []

    varcount1 = 0
    varcount2 = 0
    for l in range(I.n):
        for (i,j) in I.A:
            if Y[(l,i,j)]:
                print(l,i,j)
            solution.yvalues.append(Y[(l,i,j)])
            solution.dict_y[(l,i,j)] = varcount1
        for k in range(len(C)):
            if Z[(l,k)]:
                print(l,k)
            solution.zvalues.append(Z[(l,k)])
            solution.dict_z[(l,i,j)] = varcount2

    # solution.dict_z = Z
    # solution.dict_y = Y

    # for l in range(I.n):
    #     for (i,j) in I.A:
    #         # print((l,i,j),': ', Y[(l,i,j)])
    #         solution.yvalues.append(Y[(l,i,j)])
    #         solution.dict_y[(l,i,j)] = varcount1
    #     for k in range(len(C)):
    #         solution.zvalues.append(Z[(l,k)])
    #         solution.dict_z[(l,i,j)] = varcount2
    #         # print((l,k),': ', Z[(l,k)])


    return solution


