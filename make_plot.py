###! TEST file to compare time vs number of half-cycles for different methods
from random_orders import *
import matplotlib.pyplot as plt
from copy import deepcopy
from HCF.rules import *
from HCF.HCF import HCF


path = 'Instances/DGGKMPT/100-4.json'
K = 4
I = KEP_instance()
I.build_json_instance(path, K)




plt.title(f"Instance {I.filename}")

### random orders
k = 25
number_of_hcs, solve_time = random_orders(I, k)
plt.scatter(number_of_hcs, solve_time, label=f'Random orders ({k})', color='blue')


### betweenness centrality
J = deepcopy(I)
J.sort(betweenness_centrality(J), change = True)
solution = HCF(J)
plt.scatter(len(solution.H), solution.runtime, label='betweenness centrality', color='red') 


### min_HC's 
solution = HCF(I, method = "min")
plt.scatter(len(solution.H), solution.runtime, label = 'min hc', color = 'green')


### heuristics
solution = HCF(I, method = "heuristic")
plt.scatter(len(solution.H), solution.runtime, label = 'heuristic', color = 'mediumslateblue')
solution = HCF(I, method = "heuristic2")
plt.scatter(len(solution.H), solution.runtime, label = 'heuristic 2', color = 'blueviolet')


###
plt.legend()
plt.show()