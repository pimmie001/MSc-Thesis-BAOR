import networkx as nx


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


# TODO: 
def eigenvector_centrality(I): pass

def katz_centrality(I):pass

def clustering_coefficient():pass

def Node_Connectivity():pass