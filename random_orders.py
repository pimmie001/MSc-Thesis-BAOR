import numpy as np
from HCF.HCF import *
from EEF.EEF import *


def random_orders(I, k = 50):
    """
    For k random orders, finds the number of half-cycles and 
    corresponding ILP solve time for this order.
    """
    
    number_of_hcs = [] # number of half-cycles
    solve_time = [] # time to solve ILP model
    total_time = [] # total runtime (build + solve model)

    for _ in range(k):
        I.change_order(np.random.permutation(I.n))
        solution = HCF(I)

        number_of_hcs.append(len(solution.H))
        solve_time.append(solution.runtime)
        total_time.append(solution.total_time)

    return number_of_hcs, solve_time, total_time


def random_orders_eef(I, k = 50):
    """
    For k random orders, finds the number and variance of activated variables 
    in reduced EEF model, also returns ILP and total solve time.
    """

    number_of_variables = [] # number of activated variables
    variance_in_variables = [] # variance in number activated variables in graph
    solve_time = [] # time to solve ILP model
    total_time = [] # total time

    for _ in range(k):
        I.change_order(np.random.permutation(I.n))
        solution = EEF(I, method='REEF')

        number_of_variables.append(solution.num_vars)
        variance_in_variables.append(solution.variance)
        solve_time.append(solution.runtime)
        total_time.append(solution.total_time)

    return number_of_variables, variance_in_variables, solve_time, total_time
