import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
import itertools as it

from HCF.HCF import HCF
from HCF.min_hc import *
from HCF.min_hc_heuristics import *
from rules import *
from CYCLE.CF import *
from random_orders import random_orders
from EEF.EEF import EEF
from EEF.min_eef import *


# example HCF
# nodes = ['A', 'B', 'C', 'D']
# arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
# K = 3

# # own example EEF
# nodes = ['A', 'B', 'C', 'D']
# # nodes = ['B', 'C', 'D', 'A']
# arcs = [('A','B'), ('B','C'), ('B','D'), ('C','A'), ('C','B'), ('D','C')]
# K = 4

# ### example triforce
# nodes = [1, 2, 3, 4, 5, 6]
# arcs = [(1, 2), (2, 3), (3, 1), (2, 4), (4, 5), (5, 2), (3, 5), (5, 6), (6, 3)]
# K = 3


## example centrality measures
# nodes = list(range(1,6))
# arcs = [(1,2), (1,3), (2,3), (3,4), (2,4), (4,5)]
# K = 2

# I = KEP_instance()
# I.build_instance(arcs, nodes, K)




# for _ in range(20):
#     I.change_order(np.random.permutation(I.n))
#     print(EEF(I, get_variable_count=True))
# print()
# print(EEF(I, method='min', get_variable_count=True))



###

# path = 'Instances/DGGKMPT/100-5.json'
# # path = 'Instances/small/genjson-6.json'

# I = KEP_instance()
# I.build_json_instance(path, 4)

# sol = EEF(I)

# print(sol.time_build_model)
# print(sol.runtime)
# print(sol.obj)


########################




# for K in range(2,5):
#     for x in range(0, 10):
#         path = f'Instances/DGGKMPT/100-{str(x)}.json'

#         I = KEP_instance()
#         I.build_json_instance(path, K)

#         sol1 = EEF(I, method='REEF')
#         sol2 = EEF(I, method='min')

#         print(sol1.obj, sol2.obj)
#         if sol1.obj != sol2.obj:
#             print(K, path)




# solution1 = min_eef(I, version = 1)
# solution2 = min_eef(I, version = 2)

# print(f'obj1: {solution1.obj}')
# print(f'obj2: {solution2.obj}')

# print(f'runtime1: {solution1.runtime}')
# print(f'runtime2: {solution2.runtime}')

# print(f'vars1: {solution1.num_vars}')
# print(f'vars2: {solution2.num_vars}')

# print(f'numconstr1 {solution1.num_constrs}')
# print(f'numconstr2 {solution2.num_constrs}')


################################################################

path = 'Instances/DGGKMPT/100-4.json'
# path ='Instances/Small/genjson-0.json'
K = 5
I = KEP_instance()
I.build_json_instance(path, K)

solution = EEF(I)
print(solution.obj)
solution = EEF(I, 'heuristic')
print(solution.obj)

# print(get_cycles(I))

# solution2 = HCF(I, method = "min")

# solution3 = HCF(I, method = "heuristic")
# solution5 = HCF(I, method = "heuristic2")

# J = KEP_instance()
# J.build_json_instance(path, K)
# J.sort(betweenness_centrality(J), 'desc', change=True)
# solution4 = HCF(J)

# # print(f"value enumeration {solution.LB}")
# # print(f"value min {solution2.LB}")
# # print(f"value heuristic {solution3.LB}")



################################################################

# nodes = ['A', 'B', 'C', 'D']
# arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
# K = 3

# I = KEP_instance()
# I.build_instance(arcs, nodes, K)

# sol1 = EEF(I, method='min')
# print(f'sol1: {sol1.obj, sol1.runtime, sol1.total_time}')
# print(sol1.variance)

# print(f'sol1: {sol1.obj, sol1.time_build_model, sol1.runtime}')
# print(f'sol2: {sol2.obj, sol2.time_build_model, sol2.runtime}')

# sol2.check_feasibility()
# sol2.print_feasibility()
