from collections import Counter
import numpy as np

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HCF.min_hc import *



###########################################
############### HEURISTIC 1 ###############
###########################################


def find_most_common_value(M, completed_cycles):
    """Finds most common value in M, only considering cycles that are not completed yet"""

    flattened = []
    for k in range(len(M)):
        if k in completed_cycles:
            continue
        for l in range(len(M[k])):
            flattened.append(M[k][l][0])
            flattened.append(M[k][l][1])

    counter = Counter(flattened)
    most_common_values = counter.most_common(1)
    return most_common_values[0][0]


def check(M, indices, completed_cycles):
    """
    Checks if a half-cycle pair can be made by only adding one new half-cycle, if possible it will add this cycle and returns True
    If this is not possible will return False
    """

    success = False
    for k in range(len(M)):
        if k in completed_cycles:
            continue

        # first check if this cycle still needs to be completed
        already_completed = False
        for l in range(len(M[k])):
            if M[k][l][0] in indices and M[k][l][1] in indices:
                already_completed = True
                break
        if already_completed:
            completed_cycles.add(k)
            continue

        # if not already completed, check if it can be completed by adding only one new halfcycle
        for l in range(len(M[k])):
            if M[k][l][0] in indices:
                indices.add(M[k][l][1])
                completed_cycles.add(k)
                success = True
                break

            elif M[k][l][1] in indices:
                indices.add(M[k][l][0])
                completed_cycles.add(k)
                success = True
                break

    return success


def heuristic(I):
    """
    Heuristic solution to find minimum number of halfcycles to select for ILP model.
    First adds most common half-cycle to chosen half-cycles, then looks if a half-cycle pair 
    can be made by only adding one extra half-cycle
    """


    ## preparations
    M, c2i, H_full = determine_requirements(I)


    ## initialization
    indices = set() # indices of chosen half cycles in solution
    completed_cycles = set() # indices of cycles that already have at least one halfcycle pair
    success = False


    ## main loop
    while len(completed_cycles) < len(M):
        if not success: # add most common half-cycle
            most_common = find_most_common_value(M, completed_cycles)
            indices.add(most_common)

        success = check(M, indices, completed_cycles) # check if cycle can be made by adding one new half-cycle


    ## return solution 
    solution = choose_hc_solution(I)
    solution.name = "heuristic"
    solution.indices = list(indices)
    solution.H_full = H_full
    solution.c2i = c2i

    return solution



###########################################
############### HEURISTIC 2 ###############
###########################################


def get_count(M, num):
    # M: matrix
    # num: number of possible half-cycles (length of H_full)

    count = np.zeros(num)
    for i in range(len(M)):
        for j in range(len(M[i])):
            count[M[i][j][0]] += 1
            count[M[i][j][1]] += 1

    return count


def add_one(M, i, indices):
    one = []
    for j in range(len(M[i])):
        left = M[i][j][0]
        right = M[i][j][1]
        if left in indices:
            one.append(right)
            if right in indices:
                return True
        elif right in indices:
            one.append(left)
    return one


def heuristic2(I):
    """
    Heuristic solution to find minimum number of halfcycles to select for ILP model.
    Finds best half-cycle pair to add (product of individual occurences) untill all cycles are completed.
    If a cycle can be made by only adding one extra half-cycle, will choose the hc with the highest occurence
    """


    ### preparations
    M, c2i, H_full = determine_requirements(I)
    indices = set() # indices of chosen half cycles in solution


    ### count
    count = get_count(M, len(H_full)) # count how often each half cycle appears

    pair_rating = [] # rating of half-cycle pair is the product of individual counts
    for i in range(len(M)):
        for j in range(len(M[i])):
            pair_rating.append(count[M[i][j][0]] * count[M[i][j][1]])


    ### main loop
    k = 0
    for i in range(len(M)):
        one = add_one(M, i, indices) # need only one hc to complete pair?

        if not one: # choose 'best' pair
            # find best pair
            best = -1
            for j in range(len(M[i])):
                if pair_rating[k] > best:
                    best = pair_rating[k]
                    best_pair = j #!
                k += 1

            # add best pair
            indices.add(M[i][best_pair][0])
            indices.add(M[i][best_pair][1])


        else: # choose 'best' hc
            if one != True: # (if one == True, there already is a hc pair)
                best = -1
                for hc in one:
                    if count[hc] > best:
                        best = count[hc]
                        best_hc = hc

                indices.add(best_hc)

            k += len(M[i])


    ### return solution 
    solution = choose_hc_solution(I)
    solution.name = "heuristic2"
    solution.indices = list(indices)
    solution.H_full = H_full
    solution.c2i = c2i

    return solution



###########################################
############### HEURISTIC 3 ###############
###########################################


def heuristic3(I):
    """
    Inspired by the greedy MVC heuristic: Add the neighbor of the node with lowest support
    Similiar to heuristic 2

    Finds cycle with lowest hc pair score
    Add hc pair with best score for this cycle (= add best neigbhor)
    If only one hc pair is needed, will add the one with highest count
    """


    ### preparations
    M, c2i, H_full = determine_requirements(I)
    indices = set() # indices of chosen half cycles in solution
    indices_cycles = set() # indices of cycles that are completed


    ### count
    count = get_count(M, len(H_full)) # count how often each half cycle appears

    pair_rating = [] # rating of half-cycle pair is the product of individual counts
    for i in range(len(M)):
        for j in range(len(M[i])):
            pair_rating.append(count[M[i][j][0]] * count[M[i][j][1]])


    ### main loop
    while len(indices_cycles) < len(M):
        ### find worst pair that is left
        k = 0
        worst = float('inf')
        one = None # if changed to int: this is the best hc to add to complete a hc pair
        for i in range(len(M)):
            if i in indices_cycles:
                k += len(M[i])
                continue

            for j in range(len(M[i])):
                ## check if there are already hc included
                if M[i][j][0] in indices and M[i][j][1] in indices:
                    indices_cycles.add(i)
                    break
                if M[i][j][0] in indices:
                    if one is None or count[one] < count[M[i][j][1]]:
                        one = M[i][j][1]
                        one_i = i
                elif M[i][j][1] in indices:
                    if one is None or count[one] < count[M[i][j][0]]:
                        one = M[i][j][0]
                        one_i = i

                ## find worst pair
                if one is None and pair_rating[k+j] < worst:
                    worst = pair_rating[k]
                    worst_pair = (i,k)

            k += len(M[i])


        if len(indices_cycles) == len(M):
            break


        ### add hc or hc pair
        if one is None: # add best neighbor of worst pair
            i,k = worst_pair
            best = 0
            for j in range(len(M[i])):
                if pair_rating[k+j] > best:
                    best = pair_rating[k+j]
                    best_pair = j

            ### add best pair
            indices.add(M[i][best_pair][0])
            indices.add(M[i][best_pair][1])
            indices_cycles.add(i)

        else: # add best 'one' hc
            indices.add(one)
            indices_cycles.add(one_i)


    ### return solution 
    solution = choose_hc_solution(I)
    solution.name = "heuristic3"
    solution.indices = list(indices)
    solution.H_full = H_full
    solution.c2i = c2i

    return solution

