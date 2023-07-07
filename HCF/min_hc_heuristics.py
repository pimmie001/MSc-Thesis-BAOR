from collections import Counter

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HCF.min_hc import *



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
    solution.name = "Heuristic"
    solution.indices = list(indices)
    solution.H_full = H_full
    solution.c2i = c2i

    return solution

