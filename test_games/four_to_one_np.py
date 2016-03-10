import src.utils
from mpi4py import MPI
import numpy as np

def initial_position():
    return np.array([4])

# For possible types, see https://computing.llnl.gov/tutorials/mpi/#Routine_Arguments
def board_state_element_type():
    return MPI.INT

def gen_moves(x):
    if x[0] == 1:
        return [-1]
    return [-1, -2]

def do_move(x, move):
    return np.array([x[0] + move])

def primitive(x):
    if x[0] <= 0:
        return src.utils.LOSS
    else:
        return src.utils.UNDECIDED
