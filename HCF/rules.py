
#! not necessarily for HCF only

import networkx as nx
import numpy as np


def degree(I, Type = 'tot'):
    """
    Returns the degree of the nodes
    Type:   tot: total degree,   in: incoming degree,   out: outgoing degree
    """

    if Type == 'tot':
        I.make_pred_list()
        degree = [len(I.pred_list[i]) + len(I.adj_list[i]) for i in range(I.n)]
    elif Type == 'in':
        I.make_pred_list()
        degree = [len(I.pred_list[i]) for i in range(I.n)]
    elif Type == 'out':
        degree = [len(I.adj_list[i]) for i in range(I.n)]

    return degree



def floyd(I):
    floyd = np.full((I.n, I.n), float('inf')) # initialize matrix
    for i in I.adj_list:
        for j in I.adj_list[i]:
            floyd[i,j] = 1 # set direct neighbors distance to 1

    for i in range(I.n):
        for j in range(I.n):
            for k in range(I.n):
                floyd[j,k] = min(floyd[j,k], floyd[j,i] + floyd[i,k])

    return floyd



def closeness_centrality(I):
    """
    Returns the "Harmony Centrality Index" (modified version of closeness centrality for unconnected graphs)/
    The Harmony Centrality Index of node i is the sum (over all j != i) of the recipicle of the distance from i to j.
    """

    I.build_graph()
    floyd_mat = floyd(I)
    closeness = np.zeros(I.n)

    for i in range(I.n):
        for j in range(I.n):
            if i != j:
                closeness[i] += 1/floyd_mat[i,j]

    return closeness

    #! old closeness centrality: 
    # closeness = nx.closeness_centrality(I.G)
    # return [closeness[i] for i in range(I.n)]



def betweenness_centrality(I):
    """
    Returns the betweenness centrality of all nodes.
    The betweenness centrality of node l is the sum (over pairs (i,j)) of the ratio of the 
    number of paths i to j that contain l over the number of paths i to j.
    """

    I.build_graph()
    betweenness = nx.betweenness_centrality(I.G, normalized=False)
    return [betweenness[i] for i in range(I.n)]



def betweenness_centrality_K(I): # does not seem to work better than betweenness centrality for HCF
    """
    Returns the betweenness-K centrality of all nodes.
    The betweenness centrality of node l is the sum (over pairs (i,j)) of the ratio of the number of paths i to j of size K 
    or less that contain l over the number of paths i to j of size K or less from.
    """

    I.build_graph()

    # determine all shortest paths of size K or less
    shortest_paths = {}
    for i in range(I.n):
        for j in range(I.n):
            try:
                all_shortest_paths = nx.all_shortest_paths(I.G, source=i, target=j)
                filtered_paths = [path for path in all_shortest_paths if len(path) <= I.K + 1] # only paths of length K or less
                shortest_paths[(i,j)] = filtered_paths
            except:
                shortest_paths[(i,j)] = []

    # calcualte betweenness-K centrality
    betweenness_K = [0 for _ in range(I.n)]
    for l in range(I.n):
        for i in range(I.n):
            for j in range(I.n):
                if i != l and l != j:
                    paths = shortest_paths[(i,j)]
                    if paths:
                        count = 0
                        for path in paths:
                            count += (l in path)
                        betweenness_K[l] += count / len(paths)

    return betweenness_K

    #! OLD CODE: 
    # all_paths = dict(nx.all_pairs_shortest_path(I.G, cutoff = I.K))

    # for source in all_paths:
    #     for target in all_paths[source]:
    #         path = all_paths[source][target]
    #         for node in path[1:-1]:
    #             betweenness_K[node] += 1

    # return betweenness_K

