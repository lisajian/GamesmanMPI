from functools import reduce

WIN, LOSS, TIE, DRAW, UNDECIDED = 0, 1, 2, 3, 4
PRIMITIVES                      = (WIN, LOSS, TIE, DRAW)
PRIMITIVE_REMOTENESS            = 0
UNKNOWN_REMOTENESS              = -1
game_module                     = None # This is initialized in solve_launcher.py


# Used for logging/display purposes
STATE_MAP = {
        WIN:"win",
        LOSS:"loss",
        TIE:"tie",
        DRAW:"draw",
        UNDECIDED:"undecided"
}


def negate(state):
    """
    'Negate' a state.
    In otherwords, a WIN becomes a LOSS, otherwise preserve the states:
    TIE -> TIE
    DRAW -> DRAW
    UNDECIDED -> UNDECIDED
    """
    neg = (1, 0, 2, 3, 4)
    return neg[state]


def to_str(state):
    """
    Give an intuitive string WIN, LOSS, TIE, DRAW, UNDECIDED representation
    for a state.
    """
    str_rep = ("WIN", "LOSS", "TIE", "DRAW", "UNDECIDED")
    return str_rep[state]


def reduce_singleton(function, data):
    """
    Applies a function to *1* or more elements of a list
    as opposed to two or more for the standard reduce.
    """
    if len(data) == 1:
        return function(data[0], None)
    return reduce(function, data)
