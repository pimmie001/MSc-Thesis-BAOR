import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *
from min_hc import *


# ! todo: TEST
def HCF2(solution_hc):
    """
    Input: instance I, solution chosen halfcycles 
    Will solve the KEP using the chosen halfcycles
    ! TODO: need a (set of) constraint(s) to make sure no halfcycles of size (K+1) are created if K is odd
    """


    ### setup
    I = solution_hc.I
    H_full = solution_hc.H_full


    ### create model
    m = gp.Model('KEP HCF2')
    gp.setParam('LogFile', 'Logfiles/gurobi_hcf2.log')
    m.ModelSense = GRB.MAXIMIZE


    ### variables
    bin_vars = [] # Create a list to store the binary variables to use them in constraints later
    for i,h in enumerate(H_full):
        x = m.addVar(vtype = GRB.BINARY, obj = len(h) - 1, name = f'x_{i}')
        bin_vars.append(x)


    ### constraints (numbers refer to constraint number in HCF paper)

    ## create expressions lists
    expressions_half = [ [] for _ in range(I.n) ]   # (5)
    expressions = [ [] for _ in range(I.n) ]        # (5)
    left = [[[] for _ in range(I.n-i-1)] for i in range(I.n-1)]     # (6)
    right = [[[] for _ in range(I.n-i-1)] for i in range(I.n-1)]    # (6)


    ## add variables to expression lists
    for i,h in enumerate(H_full): # enumerating over H faster than looping over nodes
        # constraint (5):
        for j,node in enumerate(h):
            if j == 0 or j == len(h)-1: # start/end node count for halves only
                expressions_half[node].append(bin_vars[i])
            else:                       # middle nodes
                expressions[node].append(bin_vars[i])

        # constraint (6):
        start = h[0]
        end = h[-1]
        if start < end: # add to 'left' list
            left[start][end-start-1].append(bin_vars[i])
        else:           # add to 'right' list (start and end are swapped)
            right[end][start-end-1].append(bin_vars[i])


    ## add constraints to model
    for i in range(I.n):
        # constraint (5):
        expression = expressions[i]
        expression_half = expressions_half[i]
        if 0.5*len(expression_half) + len(expression) > 1:
            m.addConstr(0.5*sum(expression_half) + sum(expression) <= 1)

        # constraint (6):
        for j in range(I.n-i-1):
            if left[i][j] or right[i][j]:
                m.addConstr(sum(left[i][j]) == sum(right[i][j]))


    ## constraint for odd K
    if I.K % 2 == 1:
        indices_K = [i for i in range(len(H_full)) if len(H_full[i]) == I.K]
        for i in range(len(indices_K)):
            for j in range(i+1, len(indices_K)):
                m.addConstr(bin_vars[i] + bin_vars[j] <= 1)


    ### solve model
    # m.write("HCF 2.lp")
    # m.setParam('OutputFlag', False)
    m.optimize()

    ### make solution class
    solution = KEP_solution(I)
    solution.formulation = 'HCF 2'
    solution.optimality = m.Status == GRB.OPTIMAL
    solution.runtime = m.Runtime
    solution.num_vars = m.NumVars
    solution.num_constrs = m.NumConstrs
    solution.num_nonzero = m.NumNZs
    solution.LB = m.ObjVal # best lower bound (= objective value current solution)
    solution.UB = m.ObjBound # best upper bound
    solution.gap = m.MIPGap # optimality gap

    ### determine chosen half-cycles (for ao feasibility check)
    solution.H = H_full
    solution.indices = [v.index for v in m.getVars() if v.x > 0.5] 

    ### solve relaxation
    m_relax = m.relax()
    m_relax.setParam('OutputFlag', False)
    m_relax.optimize()
    solution.CUB = m_relax.ObjVal # continuous upper bound

    return solution

