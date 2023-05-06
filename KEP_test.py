import gurobipy as gp
from gurobipy import GRB
from find_cycles import *


# nodes = [0,1,2,3,4,5]
# arcs = [(1,5), (5,1), (0,1), (1,0), (4,0), (4,2), (2,3), (3,4)]
# K = 3 # max allowed cycle size


arcs = set()
with open('testinstance.txt') as fh:
    lines = fh.read().split('\n')
    for line in lines:
        if 'ALTERNATIVE' in line:
            continue
        if line:
            u,v,_ = line.split(',')
            arcs.add((int(u),int(v)))

n = 2048
nodes = list(range(1,n+1))
K = 3




#### create model
C = find_cycles(arcs, nodes, K)

m = gp.Model('KEP cycle formulation')


# Create a list to store the binary variables to use them in constraint later
bin_vars = []

# variables
for i in range(len(C)):
    c = C[i]
    x = m.addVar(vtype = GRB.BINARY, obj = len(c), name = f'x_{i}')
    bin_vars.append(x)


## constraints
for node in nodes:
    active_variables = []
    for i in range(len(C)):
        c = C[i]
        if node in c:
            active_variables.append(bin_vars[i])
    if active_variables:
        m.addConstr(sum(active_variables) <= 1)


# m.printStats()
# set sense and optimize
m.ModelSense = GRB.MAXIMIZE
m.optimize()

# print (m.display())


for v in m.getVars():
    if v.X:
        print('%s %g' % (v.VarName, v.X))
        

print(len(C))






### hardcode 2,3-cycles

# def get_two_cycles(arcs):
#     two_cycles = []
#     for u,v in arcs:
#         if u < v and (v,u) in arcs: # avoid double counting
#             two_cycles.append((u,v))
#     return two_cycles



######## 3-cyle werkt nu nog ALLEEN voor UNDIRECTED graphs  ###########
# def get_three_cycles(arcs):
#     three_cycles = []
#     for u,v in arcs:
#         for w in nodes:
#             if w >= u or w >= v: # avoid double counting
#                 continue 
#                 # can break if nodes are ordered (nodes = [1,2,...,n-1,n])
#             if ((u,w) in arcs and (w,v) in arcs):
#                 three_cycles.append((u,w,v))
#     return three_cycles
