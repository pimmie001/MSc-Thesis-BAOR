import numpy as np


def degree(I, type = 'tot', descending = False):
    """
    Returns the order (ascending (default) or descending) of the degree of the nodes
    type:   tot --> total degree,   in --> incoming degree,   out --> outgoing degree
    """

    if type == 'tot':
        I.make_pred_list()
        degree = [len(I.pred_list[i]) + len(I.adj_list[i]) for i in range(I.n)]
    elif type == 'in':
        I.make_pred_list()
        degree = [len(I.pred_list[i]) for i in range(I.n)]
    elif type == 'out':
        degree = [len(I.adj_list[i]) for i in range(I.n)]

    A = np.argsort(degree)
    return A[::-1] if descending else A

