import re
import numpy as np
import json
import networkx as nx


class KEP_instance:
    """
    Class instance for the KEP
    Instance attributes:
        K: maximum cycle length
        n: number of nodes
        m: number of arcs
        adj_list: adjaceny list
        pred_list: predecessor list
        adj_matrix: adjacency matrix
        index: dictionary that constains indices of nodes (e.g. index['A'] = 0)
        index_inv: inverse of the index dictionary (e.g. index_inv[0] = 'A'), used to retrieve the actual names of the nodes
    """


    def __init__(self):
        pass


    def set_K(self, K):
        self.K = K


    def build_instance(self, arcs, nodes, K=None):
        """"Builds a self-made instance"""

        self.filename = "self-made example"
        self.n = len(nodes) # number of nodes
        self.m = len(arcs) # number of edges
        if K: self.K = K


        self.index = {}
        self.index_inv = {}
        for i, node in enumerate(nodes):
            self.index[node] = i
            self.index_inv[i] = node


        # build adjacency list and matrix
        self.adj_list = {i: [] for i in range(self.n)}
        self.adj_matrix = np.zeros((self.n,self.n), dtype=int)

        for v,w in arcs:
            self.adj_list[self.index[v]].append(self.index[w])
            self.adj_matrix[self.index[v], self.index[w]] = 1


    def build_KD36_instance(self, path, K=None):
        """Builds a 'KD 00036' instance given the path and optionally also sets K"""

        if K:
            self.K = K


        with open(path) as fh:
            lines = re.split('\n', fh.read())

        for i, line in enumerate(lines):
            if '#' not in line:
                break

            if 'FILE NAME' in line:
                self.filename = re.search(r'# FILE NAME:\s*([^\s]+)', lines[0]).group(1)

            if 'NUMBER ALTERNATIVES' in line:
                self.n = int(re.search(r'\d+', line).group())
                self.index = {i+1: i for i in range(self.n)}
                self.index_inv = {i: i+1 for i in range(self.n)}

                self.adj_matrix = np.zeros((self.n,self.n), dtype=int)
                self.adj_list = {i: [] for i in range(self.n)}

            if 'NUMBER EDGES' in line:
                self.m = int(re.search(r'\d+', line).group())

        # create adj list and matrix:
        for line in lines[i:]:
            if not line:
                continue
            A = re.split(',', line)
            a, b = int(A[0])-1, int(A[1])-1 # -1 bc nodes start counting at 1

            self.adj_matrix[a, b] = 1 # add to adjacency matrix
            self.adj_list[a].append(b) # add to adjacency list


    def build_json_instance(self, path, K=None):
        """Builds a json file instance, optionally also sets K"""

        if K:
            self.K = K


        self.filename = re.search(r'([^\\/]+)$', path).group()

        with open(path) as fh:
            data = json.load(fh)['data']

        self.n = len(data)

        self.adj_matrix = np.zeros((self.n,self.n), dtype=int)
        self.adj_list = {}

        # make index and index_inv:
        self.index = {}
        self.index_inv = {}
        i = 0
        for key in data:
            self.index[int(key)] = i
            self.index_inv[i] = int(key)
            i += 1

        # make adj list and matrix: 
        for key in data:
            if 'matches' in data[key]:
                neighbors = data[key]['matches']
            else:
                neighbors = []

            u = self.index[int(key)]
            self.adj_list[u] = []
            for x in neighbors:
                n = x['recipient']
                v = self.index[n]

                self.adj_matrix[u,v] = 1
                self.adj_list[u].append(v)


    def change_order(self, order):
        """
        Takes as input a list 'order' which contains the order of the new indices.
        Will update adj_list, adj_matrix, index and index_inv according to this order
        """

        order_inv = np.argsort(order)

        index = {}
        index_inv = {}
        adj_list = {i: [] for i in range(self.n)}
        adj_matrix = np.zeros((self.n,self.n), dtype=int)


        for i in range(self.n):
            # update index and index_inv
            j = order[i]
            index[self.index_inv[j]] = i
            index_inv[i] = self.index_inv[j]

            # update adj_list and matrix
            for j in self.adj_list[i]:
                adj_matrix[order_inv[i], order_inv[j]] = 1
                adj_list[order_inv[i]].append(order_inv[j])


        # update attributes
        self.index = index
        self.index_inv = index_inv
        self.adj_list = adj_list
        self.adj_matrix = adj_matrix
        if hasattr(self, "pred_list"):
            self.make_pred_list()


    def sort(self, measure, rule, change=False):
        """
        Sorts measure based on rule (asc, desc, mid high, mid low)
        If change, will also change the order based on this order
        """

        A = np.argsort(measure)

        if rule == 'asc': # ascending
            order = A

        elif rule == 'desc': # descending
            order = A[::-1]

        elif rule == 'mid high': # higher values in the middle (e.g. [0,2,4,5,3,1])
            order = [None for _ in range(self.n)]
            for i in range(self.n):
                if i % 2 == 0:
                    order[i//2] = A[i]
                else:
                    order[-((i+1)//2)] = A[i]

        elif rule == 'mid low': # lower values in the middle (e.g. [5,3,1,0,2,4])
            order = [None for _ in range(self.n)]
            for i in range(self.n):
                if i % 2 == 0:
                    order[i//2] = A[-(i+1)]
                else:
                    order[-((i+1)//2)] = A[-(i+1)]

        if change:
            self.change_order(order)

        return order


    def make_pred_list(self):
        """Constructs predecessor list"""

        self.pred_list = {i: [] for i in range(self.n)}
        for i in range(self.n):
            for neighbor in self.adj_list[i]:
                self.pred_list[neighbor].append(i)


    def build_graph(self):
        """Builds a networkx graph of the instance (for example used to calculate closeness/centrality degree)"""

        nodes = list(range(self.n))
        arcs = []
        for i in range(self.n):
            for j in self.adj_list[i]:
                arcs.append((i,j))

        self.G = nx.DiGraph()
        self.G.add_nodes_from(nodes)
        self.G.add_edges_from(arcs)
