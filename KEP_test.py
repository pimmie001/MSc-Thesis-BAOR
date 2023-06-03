from HCF.HCF import *
from CYCLE.cycle_formulation import *
import time




path = 'Instances/small/genjson-1.json'

I = KEP_instance()
I.build_json_instance(path)
print(I.adj_list)



# nodes = ['A', 'B', 'C', 'D']
# arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
# K = 3

# I = KEP_instance()
# I.build_instance(arcs, nodes, K)

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



# path = 'Instances/Kidney Data 00036/00036-00000078.wmd'
# I = KEP_instance()
# I.build_KD36_instance(path, 3)

# I.change_order(np.random.permutation(I.n))

# solution = HCF(I)

# print(solution.indices)
# solution.show_cycles()


# st = time.time()
# solution = HCF(I)
# print()
# solution.show_summary()
# print(time.time()-st)


# st = time.time()
# solution2 = HCF(I)
# solution2.show_summary()
# print(time.time()-st)
