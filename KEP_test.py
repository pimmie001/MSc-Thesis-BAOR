from HCF.HCF import *
from HCF.min_hc import *
from HCF.min_hc_heuristics import *
from HCF.rules import *
from CYCLE.cycle_formulation import *
import time
import gurobipy as gp




# # path = 'Instances/Small/genjson-0.json'
# path = 'Instances/DGGKMPT/200-8.json'
# K = 5
# I = KEP_instance()
# I.build_json_instance(path)
# I.set_K(I.n-1)




# nodes = ['A', 'B', 'C', 'D']
# arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
# K = 4

# I = KEP_instance()
# I.build_instance(arcs, nodes)
# I.set_K(K)

# sol = heuristic(I)
# print(len(sol))



# nodes = list(range(1,8))
# arcs = [(1,2),(1,3),(1,4),(2,4),(2,3),(4,5),(5,6),(4,6),(6,7)]
# arcs = arcs + [(i,j) for (j,i) in arcs]
# I = KEP_instance()
# I.build_instance(arcs, nodes, K)

# beta_power_measure(I)
# print(sum(beta_power_measure(I).values()))

# print(I.adj_matrix)
# print(I.adj_list)
# print(I.index)
# print(I.index_inv)

# print()
# I.change_order([1,3,0,2])

# print(I.adj_matrix)
# print(I.adj_list)
# print(I.index)
# print(I.index_inv)



path = 'Instances/Kidney Data 00036/00036-00000051.wmd'
I = KEP_instance()
K = 6
I.build_KD36_instance(path, K)

st = time.time()
sol = heuristic(I)
print(len(sol))
print(time.time() - st)

# st = time.time()
# solution = HCF(I)
# print()
# solution.show_summary()
# print(time.time()-st)


# st = time.time()
# solution2 = HCF(I)
# solution2.show_summary()
# print(time.time()-st)
