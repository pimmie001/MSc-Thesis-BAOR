import numpy as np
import matplotlib.pyplot as plt
import itertools as it
from copy import deepcopy
from HCF import get_half_cycles


def exhaustive(I):
    """
    Enumerates the half-cycles n! times (for each possible order) and 
    keeps track of the number of half cycles created by each order
    """

    A = [] # list with numbers of half-cycles
    for order in it.permutations(range(I.n)):
        J = deepcopy(I)
        J.change_order(order)

        H = get_half_cycles(J)
        A.append(len(H))

    return A


def make_histogram(A):
    # Makes a histogram of the results

    bins = np.arange(min(A) - 0.5, max(A) + 1.5)
    plt.hist(A, bins=bins, edgecolor='black', alpha=0.7)
    plt.xticks(list(set(A)))
    plt.show()

