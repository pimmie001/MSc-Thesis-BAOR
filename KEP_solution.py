class KEP_solution:
    """class for solution for the KEP"""


    def __init__(self, I):
        self.I = I # solution should always correspond to an instance (I)
        self.feasibility = None # is feasible checked?


    def show_summary(self):
        print(f'Optimality: {self.optimality}')
        if not self.optimality:
            print(f'LB: {self.LB}, UB: {self.UB}')
        else:
            print(f'OBJ: {self.LB}')
        print(f'Runtime: {self.runtime}')


    def check_feasibility(self):
        if self.formulation == 'CF':
            self.feasibility = self.check_feasibility_CF()


    # ! UPDATE !!
    def check_feasibility_CF(self):
        """checks feasibility of the cycle formulation (CF) solution"""

        total_obj = 0
        all_nodes = set()
        for cycle in self.chosen_cycles:
            # check cycles not larger than K
            if len(cycle) > self.I.K: 
                return False

            # check if cycles are actually cycles
            for i in range(len(cycle)-1): 
                if not self.I.adj_matrix[cycle[i], cycle[i+1]]:
                    return False
            if not self.I.adj_matrix[cycle[-1], cycle[0]]:
                return False

            # check if nodes not already in another cycle
            for node in cycle:
                if node in all_nodes:
                    return False
                all_nodes.add(node)

            # keep track on objective
            total_obj += len(cycle)

        # check objective
        if abs(total_obj - self.LB) > 0.001:
            return False

        return True


    def print_feasibility(self):
        print(self.feasibility)
