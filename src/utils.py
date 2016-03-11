WIN, LOSS, TIE, DRAW, UNDECIDED = 1, -1, -2, 2, 0
PRIMITIVES                      = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py

# Used for logging/display purposes
STATE_MAP       = {1:"win", -1:"loss", -2:"tie", 2:"draw", 0:"undecided"}
JOB_TYPE_LIST   = ["finished", "lookup", "resolve", "send back", "distribute", "check for updates"]


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
