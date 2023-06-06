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
        if not self.optimality:
            return None

        if self.formulation == 'CF':
            self.feasibility = self.check_feasibility_CF()
        elif self.formulation == 'HCF':
            self.feasibility = self.check_feasibility_HCF()


    def check_feasibility_CF(self):
        """Checks feasibility of the cycle formulation (CF) solution"""

        total_obj = 0
        chosen_nodes = set()
        chosen_cycles = [self.I.C[i] for i in self.indices]
        for cycle in chosen_cycles:
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
                if node in chosen_nodes:
                    return False
                chosen_nodes.add(node)

            # keep track on objective
            total_obj += len(cycle)

        # check objective
        if abs(total_obj - self.LB) > 0.001:
            return False

        return True


    def check_feasibility_HCF(self):
        """Checks feasibility of HCF solution"""

        total_obj = 0
        chosen_nodes = set()
        chosen_hcycles = [self.I.H[i] for i in self.indices]
        counterparts = {} # to match half-cycles with each other
        for i, hcycle in enumerate(chosen_hcycles):
            # match half-cycle pairs:
            if (hcycle[-1], hcycle[0]) in counterparts:
                hcycle2 = chosen_hcycles[counterparts[(hcycle[-1], hcycle[0])]]
            else:
                counterparts[(hcycle[0], hcycle[-1])] = i
                continue

            # check size of cycle
            if len(hcycle) + len(hcycle2) - 2 > self.I.K:
                return False

            # check if cycles are actually cycles:
            for j in range(len(hcycle)-1):
                u,v = hcycle[j], hcycle[j+1]
                if not self.I.adj_matrix[u,v]:
                    return False
            for j in range(len(hcycle2)-1):
                u,v = hcycle2[j], hcycle2[j+1]
                if not self.I.adj_matrix[u,v]:
                    return False

            # check if nodes not already in another cycle
            for j in range(len(hcycle)):
                u = hcycle[j]
                if u in chosen_nodes:
                    return False
                chosen_nodes.add(u)
            for j in range(1, len(hcycle2)-1): # do not include begin/end because these are also in hcycle
                u = hcycle2[j]
                if u in chosen_nodes:
                    return False
                chosen_nodes.add(u)

            # keep track on objective
            total_obj += len(hcycle) + len(hcycle2) - 2


        # check if all halfcycles are matched
        if not len(counterparts) == len(chosen_hcycles)/2:
            return False

        # check objective
        if abs(total_obj - self.LB) > 0.001:
            return False

        return True


    def print_feasibility(self):
        print(self.feasibility)
