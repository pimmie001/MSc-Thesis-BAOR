import re
import numpy as np


class KEP_instance:
    """class instance for the KEP"""


    def __init__(self):
        pass


    def set_K(self, K):
        self.K = K


    def build_instance(self, arcs, nodes, K):
        self.arcs = arcs
        self.nodes = nodes
        self.K = K


    def build_KD36_instance(self, path, K=None):
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

