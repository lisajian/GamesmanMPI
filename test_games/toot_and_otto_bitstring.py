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
TOOT = "TOOT"
OTTO = "OTTO"

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
    initial_pos.append('0b1')
    return initial_pos

def primitive(board):
    def check_for_words(board):
        score = {}
        score[TOOT] = 0
        score[OTTO] = 0
        for x in range(length):
            for y in range(height):
                if board_get(board, x, y) != BLANK:
                    word = None
                    if board_get(board, x, y) == T:
                        word = TOOT
                    elif board_get(board, x, y) == O:
                        word = OTTO

                    if word_test(board, x+1, y, word, 1, 0, 1):
                        score[word] += 1
                    if word_test(board, x, y+1, word, 0, 1, 1):
                        score[word] += 1
                    if word_test(board, x+1, y+1, word, 1, 1, 1):
                        score[word] += 1
                    if word_test(board, x+1, y-1, word, 1, -1, 1):
                        score[word] += 1
        print(score)
        return score
    def word_test(board, x, y, word, dx, dy, pos):
        if pos >= 4:
            return True
        if char_rep[board_get(board, x, y)] != word[pos]:
            return False
        return word_test(board, x+dx, y+dy, word, dx, dy, pos + 1)

    score = check_for_words(board)
    if score[OTTO] == score[TOOT]:
        return src.utils.TIE if is_full(board) else src.utils.UNDECIDED
    if (score[TOOT] > score[OTTO]) ^ (is_player1_turn(board)):
        return src.utils.LOSS
    else:
        return src.utils.WIN

"""
SYMMETRY FUNCTIONS
"""

"""
TESTS AND TESTING HELPERS
"""
def print_board(board):
    rows = []
    for y in range(height):
        st = ""
        for x in range(length):
            st += char_rep[board_get(board, x, y)]
        rows.append(st)
    for row in rows[::-1]:
        print(row)
    if is_player1_turn(board):
        print("Player One's Move")
    else:
        print("Player Two's Move")

def primitive_test():
    b = initial_position()
    board_set(b, 0, 0, T)
    board_set(b, 0, 1, O)
    board_set(b, 0, 2, O)
    board_set(b, 0, 3, T)

    print_board(b)
    print(src.utils.STATE_MAP[primitive(b)])

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
        board[t_index] = False
        board[o_index] = True
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

def is_player1_turn(board):
    return board[-1]

def incr_turn(board):
    board[-1] = not board[-1]

def is_full(board):
    t_board = board[0:area]
    o_board = board[area:2 * area]
    return t_board | o_board == BitArray('0b1') * area

def board_to_bytes(board):
    return board.bytes.decode('ISO-8859-1')

# Used to unpack function input from hashable form
def bytes_to_board(data):
    a = BitArray()
    a.bytes = data.encode('ISO-8859-1')
    return a
