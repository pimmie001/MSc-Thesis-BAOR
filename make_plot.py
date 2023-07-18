###! TEST file to compare time vs number of half-cycles for different methods
from random_orders import *
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from HCF.rules import *
from HCF.HCF import HCF


path = 'Instances/DGGKMPT/200-1.json'
K = 4
I = KEP_instance()
I.build_json_instance(path, K)




plt.title(f"Instance {I.filename}")

### random orders
k = 50
number_of_hcs, solve_time = random_orders(I, k)
plt.scatter(number_of_hcs, solve_time, label=f'Random orders ({k})', color='blue')

### betweenness centrality
J = deepcopy(I)
J.sort(betweenness_centrality(J), change = True)
solution = HCF(J)
plt.scatter(len(solution.H), solution.runtime, label='betweenness centrality', color='red') 

plt.legend()
plt.show()