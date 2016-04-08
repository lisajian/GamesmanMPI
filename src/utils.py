import hashlib
import numpy as np

WIN, LOSS, TIE, DRAW, UNDECIDED = 0, 1, 2, 3, 4

PRIMITIVES                      = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py
NP                              = None # This is initialized in solve_launcher.py

# Used for logging/display purposes
STATE_MAP       = {0:"win", 1:"loss", 2:"tie", 3:"draw", 4:"undecided"}
JOB_TYPE_MAP   = {0:"finished", 1:"lookup", 2:"resolve", 3:"send back", 4:"distribute", 5:"check for updates"}


"""
The following constants help us store Job objects as NumPy arrays
for optimization purposes. POS_START_INDEX must always be the
greatest number of the first . Use these when indexing into NumPy array
representations of Jobs.
"""
JOB_TYPE_INDEX = 0
PARENT_INDEX = 1
JOB_ID_INDEX = 2
REMOTENESS_INDEX = 3
STATE_INDEX = 4
POS_START_INDEX = 5

# Used for logging/display purposes
STATE_MAP       = {0:"win", 1:"loss", 2:"tie", 3:"draw", 4:"undecided"}
JOB_TYPE_MAP   = {0:"finished", 1:"lookup", 2:"resolve", 3:"send back", 4:"distribute", 5:"check for updates"}

def negate(state):
    neg = (1, 0, 2, 3, 4)
    return neg[state]

def to_str(state):
    str_rep = ("WIN", "LOSS", "TIE", "DRAW", "UNDECIDED")
    return str_rep[state]

def symmetrical_equivalent(board):
    equivalent_boards = symmetry_recursive_helper(board, game_module.symmetry_functions())
    hashes = map(lambda board: int(hashlib.md5(str(board).encode('utf-8')).hexdigest(), 16), equivalent_boards)
    return equivalent_boards[np.argmin(hashes)]
