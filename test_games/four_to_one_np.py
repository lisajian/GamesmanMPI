import src.utils
from mpi4py import MPI

def initial_position():
    return 4

# For possible types, see https://computing.llnl.gov/tutorials/mpi/#Routine_Arguments
def board_type():
    return MPI.INT

def gen_moves(x):
    if x == 1:
        return [-1]
    return [-1, -2]

def do_move(x, move):
    return x + move

def primitive(x):
    if x <= 0:
        return src.utils.LOSS
    else:
        return src.utils.UNDECIDED
