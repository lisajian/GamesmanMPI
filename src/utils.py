WIN, LOSS, TIE, DRAW, UNDECIDED = "WIN", "LOSS", "TIE", "DRAW", "UNDECIDED"
PRIMITIVES                      = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py

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
