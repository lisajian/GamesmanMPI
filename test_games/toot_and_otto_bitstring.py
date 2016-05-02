from bitstring import BitArray
from functools import wraps
import src.utils

"""
FUN CONSTANTS
"""
length, height = 6, 4 # Feel free to edit

area = length * height
BLANK, T, O, = 0, 1, -1
char_rep = {T:"T", O:"O", BLANK:"-"}

"""
WRAPPERS FOR HASHING PROBLEMS
"""
def unpackinput(func):
    # Unpacks bytes into bitstrings
    @wraps(func)
    def wrapper(by, *args):
        return func(bytes_to_board(by), *args)
    return wrapper

def packoutput(func):
    # Packs bitstrings into bytes
    @wraps(func)
    def wrapper(*args, **kwargs):
        return board_to_bytes(func(*args, **kwargs))
    return wrapper

"""
MAIN GAME LOGIC
"""
def initial_position():
    initial_pos = BitArray('0b0') * area * 2
    hand = BitArray('0b0110')
    initial_pos.append(hand * 4)
    return initial_pos

"""
SYMMETRY FUNCTIONS
"""

"""
HELPER FUNCTIONS FOR BIT MANIPULATION
STOP SCROLLING IF YOU CARE ABOUT READABILITY
"""
# Gets the letter of an (x, y) coordinate in board
def board_get(board, x, y):
    if board[int(length  * y + x)]:
        return T
    elif board[int(area + length * y + x)]:
        return O
    else:
        return BLANK

# Sets (x, y) on board to letter
def board_set(board, x, y, letter):
    t_index = int(length * y + x)
    o_index = int(area + length * y + x)
    if letter == T:
        board[t_index] = True
        board[o_index] = False
    elif letter == O:
        board[t_index] = True
        board[o_index] = False
    else:
        board[t_index] = False
        board[o_index] = False

# Returns letters left for Player 1 or Player 2 on board
def get_hand_count(board, player, letter):
    player_offset = 8 * (player - 1)
    hand_offset = 0 if letter == T else 4
    start_index = area * 2 + player_offset + hand_offset

    return board[start_index:start_index + 4].int

# Decrements player 1 or player 2's number of letter in hand on board
def decr_hand_count(board, player, letter):
    player_offset = 8 * (player - 1)
    hand_offset = 0 if letter == T else 4
    start_index = area * 2 + player_offset + hand_offset

    new_count = board[start_index:start_index + 4].int - 1
    board[start_index:start_index + 4] = new_count

def board_to_bytes(board):
    return board.bytes.decode('ISO-8859-1')

# Used to unpack function input from hashable form
def bytes_to_board(data):
    a = BitArray()
    a.bytes = data.encode('ISO-8859-1')
    return a
