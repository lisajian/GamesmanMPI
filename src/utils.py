from functools import reduce

WIN, LOSS, TIE, DRAW, UNDECIDED = 0, 1, 2, 3, 4
PRIMITIVES                      = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py


# Used for logging/display purposes
STATE_MAP       = {0:"win", 1:"loss", 2:"tie", 3:"draw", 4:"undecided"}


def negate(state):
    neg = (1, 0, 2, 3, 4)
    return neg[state]


def to_str(state):
    str_rep = ("WIN", "LOSS", "TIE", "DRAW", "UNDECIDED")
    return str_rep[state]


def reduce_helper(function, data):
    if len(data) == 1:
        return function(data[0], None)
    return reduce(function, data)
