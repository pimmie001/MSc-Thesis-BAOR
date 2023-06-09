# from HCF.HCF import *
# from HCF.HCF2 import *
import pandas as pd
import matplotlib.pyplot as plt
from HCF.min_hc import *
from HCF.min_hc_heuristics import *
from HCF.rules import *
from CYCLE.cycle_formulation import *
from copy import deepcopy


from HCF.HCF_new import HCF
from random_orders import random_orders



# path = 'Instances/Small/genjson-0.json'
path = 'Instances/DGGKMPT/200-1.json'
K = 4
I = KEP_instance()
I.build_json_instance(path, K)

k = 50
number_of_hcs, solve_time = random_orders(I, k)

print(solve_time)
print(number_of_hcs)
plt.scatter(number_of_hcs, solve_time)
plt.title(f"Instance {I.filename}, k = {k}")
plt.show()



#####################################

# solution = HCF(I)

# solution2 = HCF(I, method = "min")

# solution3 = HCF(I, method = "heuristic")

# J = KEP_instance()
# J.build_json_instance(path, K)
# J.sort(betweenness_centrality(J), 'desc', change=True)
# solution4 = HCF(J)

# # print(f"value enumeration {solution.LB}")
# # print(f"value min {solution2.LB}")
# # print(f"value heuristic {solution3.LB}")

# df = pd.DataFrame(index = ['enumeration', 'min', 'heuristic', 'rule'], columns = ['obj', 'time H', 'time build model', 'time solve model', 'total time'])



# df.loc['enumeration']   = [solution.LB, solution.time_find_H, solution.time_build_model, solution.runtime, solution.time_find_H + solution.time_build_model + solution.runtime]
# df.loc['min']           = [solution2.LB, solution2.time_find_H, solution2.time_build_model, solution2.runtime, solution2.time_find_H + solution2.time_build_model + solution2.runtime]
# df.loc['heuristic']     = [solution3.LB, solution3.time_find_H, solution3.time_build_model, solution3.runtime, solution3.time_find_H + solution3.time_build_model + solution3.runtime]
# df.loc['rule']          = [solution4.LB, solution4.time_find_H, solution4.time_build_model, solution4.runtime, solution4.time_find_H + solution4.time_build_model + solution4.runtime]

# print('\n')
# print(df)

# nodes = ['A', 'B', 'C', 'D']
# arcs = [('A','B'), ('B','D'), ('D','C'), ('C','A'), ('B','C'), ('C','B')]
# K = 4

# I = KEP_instance()
# I.build_instance(arcs, nodes)
# I.set_K(K)

# sol = heuristic(I)
# print(len(sol))





# path = 'Instances/DGGKMPT/200-2.json'
# I = KEP_instance()
# K = 4
# I.build_json_instance(path, K)





###########################################

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

