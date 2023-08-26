import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy

from HCF.HCF import HCF
from HCF.min_hc import *
from HCF.min_hc_heuristics import *
from HCF.rules import *
from CYCLE.CF import *
from random_orders import random_orders
from EEF.EEF import EEF
from EEF.REEF import floyd_matrix, REEF
from EEF.min_eef import min_eef


from EEF.REEF2 import REEF2




path = 'Instances/DGGKMPT/200-5.json'
# path = 'Instances/small/genjson-0.json'
K = 4
I = KEP_instance()
I.build_json_instance(path, K)

sol1 = REEF(I)
sol2 = REEF2(I)

print(f'sol1: {sol1.obj, sol1.time_build_model, sol1.runtime}')
print(f'sol2: {sol2.obj, sol2.time_build_model, sol2.runtime}')

# sol2.check_feasibility()
# sol2.print_feasibility()


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

# path = 'Instances/DGGKMPT/200-1.json'
# K = 4
# I = KEP_instance()
# I.build_json_instance(path, K)

# solution = HCF(I)

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

# df = pd.DataFrame(index = ['enumeration', 'min', 'heuristic', 'heuristic2', 'rule'], columns = ['obj', 'time H', 'time build model', 'time solve model', 'total time'])



# df.loc['enumeration']   = [solution.LB, solution.time_find_H, solution.time_build_model, solution.runtime, solution.time_find_H + solution.time_build_model + solution.runtime]
# df.loc['min']           = [solution2.LB, solution2.time_find_H, solution2.time_build_model, solution2.runtime, solution2.time_find_H + solution2.time_build_model + solution2.runtime]
# df.loc['heuristic']     = [solution3.LB, solution3.time_find_H, solution3.time_build_model, solution3.runtime, solution3.time_find_H + solution3.time_build_model + solution3.runtime]
# df.loc['heuristic2']    = [solution5.LB, solution5.time_find_H, solution5.time_build_model, solution5.runtime, solution5.time_find_H + solution5.time_build_model + solution5.runtime]
# df.loc['rule']          = [solution4.LB, solution4.time_find_H, solution4.time_build_model, solution4.runtime, solution4.time_find_H + solution4.time_build_model + solution4.runtime]

# print('\n')
# print(df)


################################################################

# nodes = ['A', 'B', 'C', 'D']
# arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
# K = 4

# I = KEP_instance()
# I.build_instance(arcs, nodes, K)

# sol1 = REEF(I)
# sol2 = REEF2(I)

# print(f'sol1: {sol1.obj, sol1.time_build_model, sol1.runtime}')
# print(f'sol2: {sol2.obj, sol2.time_build_model, sol2.runtime}')

# sol2.check_feasibility()
# sol2.print_feasibility()


################################################################

# # HCF
# solution_hcf = HCF(I)

# # Heuristic
# solution_hc = heuristic(I)
# solution_heur = HCF2(solution_hc)

# # Min # of half-cycles
# solution_hc2 = min_hc(I)
# solution_hcf2 = HCF2(solution_hc2)

# # Rule
# J = KEP_instance()
# J.build_json_instance(path, K)
# measure = betweenness_centrality(J)
# J.sort(measure, 'desc', change=True)
# solution_rule = HCF(J)

# print('\n\n')
# print(f'solution HCF: {solution_hcf.runtime}')
# print(f'solution heuristic: {solution_heur.runtime}')
# print(f'solution HCF2 min hc: {solution_hcf2.runtime}')
# print(f'solution rule: {solution_rule.runtime}\n')

# print(len(get_half_cycles(I)))
# print(len(solution_hc.indices))
# print(len(solution_hc2.indices))
# print(len(get_half_cycles(J)))

