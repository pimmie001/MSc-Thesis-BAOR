import re
import numpy as np


class KEP_instance:
    """Class instance for the KEP"""


    def __init__(self):
        pass


    def set_K(self, K):
        self.K = K


    def build_instance(self, arcs, nodes, K):
        """"build self made instance"""

        self.filename = "self-made example"
        # self.arcs = arcs
        self.n = len(nodes) # number of nodes
        self.m = len(arcs) # number of edges
        # self.nodes = np.arange(self.n) # the indices of nodes # TODO: remove this?
        self.K = K


        nodes_inv = {} # inverse of nodes. E.g. if nodes[i] = 'A' then nodes_inv[A] = i, important for ordering nodes
        for i, node in enumerate(nodes):
            nodes_inv[node] = i


        # build adjacency list and matrix
        self.adj_list = {}
        for i in range(self.n):
            self.adj_list[i] = []

        self.adj_matrix = np.zeros((self.n,self.n), dtype=int)

        for v,w in arcs:
            self.adj_list[nodes_inv[v]].append(nodes_inv[w])
            self.adj_matrix[nodes_inv[v], nodes_inv[w]] = 1


    def build_KD36_instance(self, path, K=None, index=None):
        """
        Build a 'KD 00036' instance given the path and optionally also sets K
        Index specifies the order of the nodes (used for symmetry reduction)
        """

        if K:
            self.K = K

        self.adj_list = {} # adjacency list

        with open(path) as fh:
            lines = re.split('\n', fh.read())

        for i, line in enumerate(lines):
            if '#' not in line:
                break

            if 'FILE NAME' in line:
                self.filename = re.search(r'# FILE NAME:\s*([^\s]+)', lines[0]).group(1)

            if 'NUMBER ALTERNATIVES' in line:
                self.n = int(re.search(r'\d+', line).group())
                self.nodes = np.arange(self.n)
                self.adj_matrix = np.zeros((self.n,self.n), dtype=int) # adjacency matrix
                for i in range(self.n):
                    self.adj_list[i] = []

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


    # ! needs testing
    def change_order(self, order):
        """
        Updates adj_list and adj_matrix with new node order
        """

        # find nodes inverse
        nodes_inv = {} # inverse of nodes. E.g. if nodes[i] = 'A' then nodes_inv[A] = i, important for ordering nodes
        for i, node in enumerate(order):
            nodes_inv[node] = i

        # build adj list and matrix
        adj_list = {}
        for i in range(self.n):
            adj_list[i] = []

        adj_matrix = np.zeros((self.n,self.n), dtype=int)

        for v in range(self.n):
            for w in self.adj_list[v]:
                adj_list[nodes_inv[v]].append(nodes_inv[w])
            adj_matrix[nodes_inv[v], nodes_inv[w]] = 1

        # update adj list and matrix
        self.adj_list = adj_list
        self.adj_matrix = adj_matrix

