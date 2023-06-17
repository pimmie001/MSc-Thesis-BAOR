import networkx as nx
import numpy as np



def degree(I, Type = 'tot'):
    """
    Returns the degree of the nodes
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



def closeness_centrality(I):
    """The closeness centrality of a node is the sum of the distance to every other node (distance = n if not possible)"""
    I.build_graph()
    closeness = nx.closeness_centrality(I.G)
    return [closeness[i] for i in range(I.n)]



def betweenness_centrality(I):
    """The betweenness centrality of a node is the amount of times the node lies on a shortest path between other nodes"""
    I.build_graph()
    betweenness = nx.betweenness_centrality(I.G, normalized=False)
    return [betweenness[i] for i in range(I.n)]



# def floyd_matrix(I):
#     # returns floyd matrix

#     floyd = np.full((I.n, I.n), I.n) # initialize matrix
#     for i in I.adj_list: 
#         for j in I.adj_list[i]:
#             floyd[i,j] = 1 # set direct neighbors distance to 1

#     for i in range(I.n):
#         for j in range(I.n):
#             for k in range(I.n):
#                 floyd[j,k] = min(floyd[j,k], floyd[j,i] + floyd[i,k])

#     return floyd


#! TODO: improve efficiency
def betweenness_centrality_K(I):
    """The betweenness centrality of a node is the amount of times the node lies on a shortest path of size K or less between other nodes"""
    I.build_graph()

    betweenness_K = [0 for _ in range(I.n)]
    all_paths = dict(nx.all_pairs_shortest_path(I.G, cutoff = I.K))
    for source in all_paths:
        for target in all_paths[source]:
            path = all_paths[source][target]
            for node in path[1:-1]:
                betweenness_K[node] += 1

    return betweenness_K

    # ODNF = floyd_matrix(I)

    # betweenness_K = np.zeros(I.n)
    # for a in range(I.n):
    #     for b in range(I.n):
    #         if a == b or ODNF[a, b] > min(I.K, I.n-1):
    #             continue

    #         all_paths = nx.all_shortest_paths(I.G, a, b)

    #         between_nodes = np.zeros(I.n, dtype=int)
    #         num_paths = 0
    #         for path in all_paths:
    #             num_paths += 1
    #             for i in path[1:-1]:
    #                 between_nodes[i] += 1

    #         for i in range(I.n):
    #             betweenness_K[i] += between_nodes[i]/num_paths

    # return betweenness_K


# ! ?
def beta_power_measure(I): # ! CHECK?
    # ...

    I.build_graph()
    graph = I.G

    beta_power = {}
    for node in graph.nodes:
        neighbors = list(graph.neighbors(node))
        node_degree = graph.degree(node)
        neighbor_sum = sum(graph.degree(neighbor) for neighbor in neighbors)
        
        if node_degree + neighbor_sum != 0:
            beta_power[node] = neighbor_sum / (node_degree + neighbor_sum)
        else:
            beta_power[node] = 0.0
    print(beta_power)
    return beta_power




# ! functions below are tested and do not improve against desc total degree

# # TODO: 
# def Eigenvector_centrality(I): 
#     I.build_graph()
#     centrality = nx.eigenvector_centrality(I.G)
#     return [centrality[i] for i in range(I.n)]


# def Katz_centrality(I):
#     I.build_graph()
#     try:
#         katz_centrality = nx.katz_centrality(I.G)
#         return [katz_centrality[i] for i in range(I.n)]
#     except:
#         return None


# def clustering_coefficient(I):
#     I.build_graph()
#     coefficients = nx.clustering(I.G)
#     return [coefficients[i] for i in range(I.n)]


# def Node_Connectivity(I):
#     I.build_graph()
#     connectivity = nx.node_connectivity(I.G)
#     print(connectivity)
#     return [connectivity[i] for i in range(I.n)]

