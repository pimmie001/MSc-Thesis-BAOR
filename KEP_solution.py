class KEP_solution:
    """class for solution for the KEP"""


    def __init__(self, I):
        self.I = I # solution should always correspond to an instance (I)
        self.feasible_check = None # is feasible checked?


    def show_summary(self):
        print(f'Optimality: {self.optimality}')
        if not self.optimality:
            print(f'LB: {self.LB}, UB: {self.UB}')
        else:
            print(f'OBJ: {self.LB}')
        print(f'Runtime: {self.runtime}')


    def check_feasibility(self):
        pass # TODO 


    def print_feasibility(self):
        print(self.feasible_check)