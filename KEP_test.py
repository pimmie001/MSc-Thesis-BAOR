from HCF.HCF_new import *
from CYCLE.cycle_formulation import *
import time


nodes = ['A', 'B', 'C', 'D']
arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
K = 4

I = KEP_instance()
I.build_instance(arcs, nodes, K)


path = 'Instances/Kidney Data 00036/00036-00000118.wmd'
I = KEP_instance()
I.build_KD36_instance(path, 4)


st = time.time()
solution = HCF(I)
print()
solution.show_summary()
print(time.time()-st)


# st = time.time()
# solution2 = HCF(I)
# solution2.show_summary()
# print(time.time()-st)
