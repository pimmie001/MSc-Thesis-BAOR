import re
import numpy as np


class KEP_instance:
    """class instance for the KEP"""


    def __init__(self):
        pass


    def set_K(self, K):
        self.K = K


    def build_instance(self, arcs, nodes, K):
        # build self made instance

        self.arcs = arcs
        self.nodes = nodes
        self.K = K

        self.n = len(nodes)
        self.m = len(arcs)


        nodes_inv = {} # inverse of nodes. I.e. if nodes[i] = 'A' then nodes_inv[A] = i
        for i, node in enumerate(nodes):
            nodes_inv[node] = i


        # build adjacency list and matrix
        self.adj_list = {}
        self.adj_matrix = np.zeros((self.n,self.n), dtype=int)

        for v,w in arcs:
            if v not in self.adj_list:
                self.adj_list = [w]
            else:
                self.adj_list.append(w)

            self.adj_matrix[nodes_inv[v], nodes_inv[w]] = 1


    def build_KD36_instance(self, path, K=None):
        # build a KD 00036 instance given the path. optionally also sets K

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
            if 'NUMBER EDGES' in line:
                self.m = int(re.search(r'\d+', line).group())


        self.adj_list = {} # adjacency list
        self.adj_matrix = np.zeros((self.n,self.n), dtype=int) # adjacency matrix

        for line in lines[i:]:
            if not line:
                continue
            A = re.split(',', line)
            a, b = int(A[0]), int(A[1])

            # add to adjacency matrix
            self.adj_matrix[a-1, b-1] = 1

            # add to adjacency list
            if a not in self.adj_list:
                self.adj_list[a] = [b]
            else:
                self.adj_list[a].append(b)

