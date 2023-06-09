import numpy as np


def make_floyd(I):
    # returns floyd matrix

    floyd = np.full((I.n, I.n), I.n) # initialize matrix
    for i in I.adj_list: 
        for j in I.adj_list[i]:
            floyd[i,j] = 1 # set direct neighbors distance to 1

    for i in range(I.n):
        for j in range(I.n):
            for k in range(I.n):
                floyd[j,k] = min(floyd[j,k], floyd[j,i] + floyd[i,k])

    return floyd



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

    order = np.argsort(degree)
    return order[::-1] if descending else order


def betweenness_centrality(I):
    """The betweenness centrality of a node is the amount of times the node lies on a shortest path between other nodes"""

    floyd = make_floyd(I)
    betweenness = np.zeros(I.n)
    for i in range(I.n):
        for j in range(I.n):
            for k in range(j+1, I.n):
                pass
                # betweenness[i] += floyd[i,k] < floyd[j,k] # ! NOT correct!!!
    return betweenness


def closeness_centrality(I):
    """The closeness centrality of a node is the sum of the distance to every other node (distance = n if not possible)"""

    floyd = make_floyd(I)
    closeness = np.zeros(I.n)
    for i in range(I.n):
        for j in range(I.n):
            if i != j:
                closeness[i] += floyd[i,j]
    return closeness

