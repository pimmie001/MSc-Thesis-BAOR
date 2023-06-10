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
    I.build_graph()
    closeness = nx.closeness_centrality(I.G)
    return [closeness[i] for i in range(I.n)]



def betweenness_centrality(I):
    """The betweenness centrality of a node is the amount of times the node lies on a shortest path between other nodes"""
    I.build_graph()
    betweenness = nx.betweenness_centrality(I.G, normalized=False)
    return [betweenness[i] for i in range(I.n)]

