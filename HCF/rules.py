import numpy as np
import networkx as nx


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

    return degree
    # order = np.argsort(degree)
    # return order[::-1] if descending else order



def floyd_matrix(I):
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


def closeness_centrality(I):
    """The closeness centrality of a node is the sum of the distance to every other node (distance = n if not possible)"""

    floyd = floyd_matrix(I)
    closeness = np.zeros(I.n, dtype=int)
    for i in range(I.n):
        for j in range(I.n):
            if i != j:
                closeness[i] += floyd[i,j]
    return closeness


def closeness_centrality2(I):
    I.build_graph()
    closeness = nx.closeness_centrality(I.G)
    return [closeness[i] for i in range(I.n)]


def betweenness_centrality(I):
    """The betweenness centrality of a node is the amount of times the node lies on a shortest path between other nodes"""
    I.build_graph()
    betweenness = nx.betweenness_centrality(I.G, normalized=False)
    return [betweenness[i] for i in range(I.n)]




###### OLD CODE: 


# def floyd_with_pred(I):
#     # floyd algorithm that also returns pred list

#     n = I.n
#     dist = [[float('inf') for _ in range(n)] for _ in range(n)]
#     pred = [[None for _ in range(n)] for _ in range(n)]

#     # Initialize
#     for i in range(n):
#         for j in range(n):
#             if i == j:
#                 dist[i][j] = 0
#             elif I.adj_matrix[i][j] == 1:
#                 dist[i][j] = 1
#                 pred[i][j] = i

#     # Floyd-Warshall algorithm
#     for k in range(n):
#         for i in range(n):
#             for j in range(n):
#                 if dist[i][j] > dist[i][k] + dist[k][j]:
#                     dist[i][j] = dist[i][k] + dist[k][j]
#                     pred[i][j] = pred[k][j]

#     return dist, pred


# def reconstruct_path(pred, source, destination):
#     if pred[source][destination] is None:
#         return [] # No path exists

#     path = [] # path will not include source or destination
#     while destination != source:
#         destination = pred[source][destination]
#         if destination == source:
#             break
#         path.append(destination)

#     return path # paths are returned in reverse order but that does not matter


# def betweenness_centrality(I):
#     """The betweenness centrality of a node is the amount of times the node lies on a shortest path between other nodes"""

#     dist, pred = floyd_with_pred(I) # also returns predecessor matrix

#     # find all paths that have in-between nodes:
#     all_paths = []
#     for source in range(I.n):
#         for destination in range(I.n):
#             if dist[source][destination] > 1: # consider only paths that have an in-between node
#                 path = reconstruct_path(pred, source, destination)
#                 all_paths.append(path)

#     # calculate betweenness:
#     betweenness = np.zeros(I.n, dtype=int)
#     for path in all_paths:
#         for node in path:
#             betweenness[node] += 1

#     return betweenness