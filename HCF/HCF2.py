import numpy as np
import gurobipy as gp
from gurobipy import GRB

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from KEP_instance import *
from KEP_solution import *

from model import *


def HCF2(I):
    """
    Given instance I, will find minimum number of halfcycles using model.model.
    Then solves the HCF using this ILP formulation
    TODO: need (a set of) constraint(s) to make sure no halfcycles of size (K+1) are created if K is odd
    """
    pass