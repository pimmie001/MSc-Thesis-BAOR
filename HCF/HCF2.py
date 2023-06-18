import numpy as np
import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *

from min_hc import *


def HCF2(I): #! make so that input is chosen halfcylces (need not be minimum if e.g. heuristic is used)
    """
    Input: instance I, chosen halfcycles 
    Will solve the KEP using the chosen halfcycles
    ! TODO: need a (set of) constraint(s) to make sure no halfcycles of size (K+1) are created if K is odd
    ! if K is even, not needed
    """
    pass