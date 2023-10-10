###! TEST file to compare time vs number of half-cycles for different methods
from random_orders import *
import matplotlib.pyplot as plt
from copy import deepcopy
from rules import *
from HCF.HCF import HCF
from EEF.EEF import EEF
from EEF.min_eef import min_eef
import os 
import pandas as pd

#!!! TODO: clean and rename (and maybe split) this file


def get_numeric_part(filename):
    # makes sure that files with smaller n get run first so they dont get stuck 
    # Assuming the filenames are of the format 'x-y.json'
    parts = filename.split('.')[0].split('-')
    numeric_part1 = int(parts[0])  # '50'
    numeric_part2 = int(parts[1])  # '0' to '11'
    return numeric_part1, numeric_part2



folder_path = 'Instances/DGGKMPT'

file_names = os.listdir(folder_path)
sorted_file_names = sorted(file_names, key=get_numeric_part)

columns = [f'random order {i+1}' for i in range(50)] + ['betweenness centrality', 'ILP']
# # columns = ['vars', 'variance', 'ilp time', 'total time']
df = pd.DataFrame(columns=columns)

save_folder = r'C:\Users\pimvk\OneDrive\Documents\Studie\University\Master\Thesis BAOR\Results\EEF' # DESKTOP

for file_name in sorted_file_names:
    if not file_name.endswith('.json'):
        continue
    print(file_name)

    file_path = os.path.join(folder_path, file_name)

    I = KEP_instance()
    I.build_json_instance(file_path)


    ######## Save in table ########
    for K in [4, 5, 6]:
        I.set_K(K)

        ### random orders
        if I.n <= 50:
            k = 50
        elif I.n <= 100:
            k = 25
        elif I.n <= 200:
            k = 10
        else:
            k = 5


        instance_name = f'{file_name}, K = {K}'

        number_of_variables, variance_in_variables, solve_time, total_time = random_orders_eef(I, k=k)
        for i in range(k):
            df.loc[instance_name, f'random order {i+1}'] = (number_of_variables[i], variance_in_variables[i], solve_time[i], total_time[i])


        ### betweenness centrality
        J = deepcopy(I)
        J.sort(betweenness_centrality(J), change = True)
        solution_BC = EEF(J)

        df.loc[instance_name, 'betweenness centrality'] = (solution_BC.num_vars, solution_BC.variance, solution_BC.runtime, solution_BC.total_time)


        ### min_HC's
        solution_min = EEF(I, method='min')
        df.loc[instance_name, 'ILP'] = (solution_min.num_vars, solution_min.variance, solution_min.runtime, solution_min.total_time)


        ### heuristics #! (no heuristics yet for EEF)
        # todo

        ### write to excel sheet
        df.to_excel(save_folder + '\\' + 'results EEF 01-09.xlsx')







# ##################################################################################

# from random_orders import *
# import matplotlib.pyplot as plt
# from copy import deepcopy
# from HCF.rules import *
# from HCF.HCF import HCF



# def get_numeric_part(filename):
#     # makes sure that files with smaller n get run first so they dont get stuck 
#     # Assuming the filenames are of the format 'x-y.json'
#     parts = filename.split('.')[0].split('-')
#     numeric_part1 = int(parts[0])  # '50'
#     numeric_part2 = int(parts[1])  # '0' to '11'
#     return numeric_part1, numeric_part2



# folder_path = 'Instances/DGGKMPT'

# file_names = os.listdir(folder_path)
# sorted_file_names = sorted(file_names, key=get_numeric_part)

# for file_name in sorted_file_names:
#     if not file_name.endswith('.json'):
#         continue
#     print(file_name)

#     file_path = os.path.join(folder_path, file_name)

#     I = KEP_instance()
#     I.build_json_instance(file_path)


#     for K in [4, 6]:
#         I.set_K(K)


#         ######## run + plot time given H ########

#         ### random orders

#         if I.n <= 50:
#             k = 50
#         elif I.n <= 100:
#             k = 25
#         elif I.n <= 200:
#             k = 10
#         else:
#             k = 5

#         number_of_hcs, solve_time, total_time = random_orders(I, k=k)
#         plt.scatter(number_of_hcs, solve_time, label=f'Random orders ({k})', color='blue')


#         ### heuristics
#         solution_H1 = HCF(I, method = "heuristic")
#         plt.scatter(len(solution_H1.H), solution_H1.runtime, label='heuristic', color='mediumslateblue')
#         solution_H2 = HCF(I, method = "heuristic2")
#         plt.scatter(len(solution_H2.H), solution_H2.runtime, label='heuristic 2', color='blueviolet')


#         ### betweenness centrality
#         J = deepcopy(I)
#         J.sort(betweenness_centrality(J), change = True)
#         solution_BC = HCF(J)
#         plt.scatter(len(solution_BC.H), solution_BC.runtime, label='betweenness centrality', color='red') 


#         ### min_HC's 
#         solution_min = HCF(I, method = "min")
#         plt.scatter(len(solution_min.H), solution_min.runtime, label='min hc' + ' (suboptimal)'*(not solution_min.solution_hc.optimality) , color='green')


#         ### other stuff
#         title = f"Instance {I.filename} (K = {I.K}) given H"
#         plt.title(title)
#         plt.legend()
#         plt.xlabel("Number of half-cycles in ILP model")
#         plt.ylabel("Time to solve HCF given H")

#         # save and close plot
#         save_folder = r'C:\Users\pimvk\OneDrive\Documents\Studie\University\Master\Thesis BAOR\Results\Time vs num hcs' # DESKTOP
#         filename = save_folder + '\\' + title + '.png'
#         plt.savefig(filename)
#         plt.close()






#         ######## plot total time ########

#         ### random orders
#         plt.scatter(number_of_hcs, total_time, label=f'Random orders ({k})', color='blue')


#         ### heuristics
#         plt.scatter(len(solution_H1.H), solution_H1.total_time, label='heuristic', color='mediumslateblue')
#         plt.scatter(len(solution_H2.H), solution_H2.total_time, label='heuristic 2', color='blueviolet')


#         ### betweenness centrality
#         plt.scatter(len(solution_BC.H), solution_BC.total_time, label='betweenness centrality', color='red') 


#         ### min_HC's 
#         plt.scatter(len(solution_min.H), solution_min.total_time, label='min hc' + ' (suboptimal)'*(not solution_min.solution_hc.optimality) , color='green')


#         ### other stuff
#         title = f"Instance {I.filename} (K = {I.K}) total time"
#         plt.title(title)
#         plt.legend()
#         plt.xlabel("Number of half-cycles in ILP model")
#         plt.ylabel("Total time to solve HCF")

#         # save and close plot
#         filename = save_folder + '\\' + title + '.png'
#         plt.savefig(filename)
#         plt.close()


