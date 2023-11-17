import sys, os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from EEF.min_eef import *
from CYCLE.CF import get_cycles


###########################################
############### HEURISTIC 1 ###############
###########################################


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
    cycles_nodes = [[] for _ in range(n)]
    indices_cycles = [[] for _ in range(n)]
    for i,cycle in enumerate(C):
        if i in exclude:
            continue
        for node in cycle:
            count[node] += 1
            cycles_nodes[node].append(cycle)
            indices_cycles[node].append(i)
    return count, cycles_nodes, indices_cycles



def heuristic_eef(I):
    """
    Heuristic solution for finding minimum number of activated variables in the EEF.
    Finds most common node in cycles that are not yet added, adds the arcs in the cycles
    that contain this node. Repeat process until all cycles are added.
    """

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
    while len(added) < len(C): # all cycles need to be able to be made
        ## find most common node left
        count, cycles_nodes, indices_cycles = count_nodes(I.n, C, added) # count occurences of nodes
        l = np.argmax(count)
        C_i = cycles_nodes[l]

        ## find which cycles include this node
        for i in indices_cycles[l]:
            Z[(l,i)] = 1
            added.add(i)

        ## activate arcs corresponding to chosen cycles
        for cycle in C_i:
            for (a,b) in arcs_in_cycle(cycle):
                Y[(l,a,b)] = 1


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
            solution.dict_y[(l,i,j)] = varcount1
            solution.yvalues.append(Y[(l,i,j)])
            varcount1 += 1
        for k in range(len(C)):
            solution.dict_z[(l,k)] = varcount2
            solution.zvalues.append(Z[(l,k)])
            varcount2 += 1

    return solution

