import numpy as np


def degree(I, Type = 'tot', descending = False):
    """
    Returns the order (ascending (default) or descending) of the degree of the nodes
    Type:   tot --> total degree,   in --> incoming degree,   out --> outgoing degree
    """

    if Type == 'tot':
        I.make_pred_list()
        degree = [len(I.pred_list[i]) + len(I.adj_list[i]) for i in range(I.n)]
    elif Type == 'in':
        I.make_pred_list()
        degree = [len(I.pred_list[i]) for i in range(I.n)]
    elif Type == 'out':
        degree = [len(I.adj_list[i]) for i in range(I.n)]

    A = np.argsort(degree)
    return A[::-1] if descending else A

