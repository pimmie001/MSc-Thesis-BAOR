class KEP_solution:
    """class for solution for the KEP"""


    def __init__(self, I):
        self.I = I # solution should always correspond to an instance (I)
        self.feasible_check = None # is feasible checked?


    def check_feasibility(self):
        pass # TODO 


    def print_feasibility(self):
        print(self.feasible_check)