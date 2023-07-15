import numpy as np
from HCF.HCF import *


def random_orders(I, k = 1000):
    """For k random orders, finds the number of half-cycles and corresponding ILP solve time for this order"""
    
    number_of_hcs = [] # number of half-cycles
    solve_time = [] # time to solve ILP model 

    for _ in range(k):
        I.change_order(np.random.permutation(I.n))
        solution = HCF(I)

        number_of_hcs.append(len(solution.H))
        solve_time.append(solution.runtime)

    return number_of_hcs, solve_time

