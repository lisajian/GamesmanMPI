import numpy as np
from numpy import *
from mpi4py import MPI

#Toot and Otto game implementation for Gamescrafters

#defines the state object for the toot and otto game
#state keeps track of 4 things:
#the player whose turn it is, the board, and both players hands
#additional methods are helper methods for the neccessary solver functions and
class State(object):
    """Base State class"""
    """0 for blank space, 1 for T, 2 for O"""
    toot = np.array([1,2,2,1])
    otto = np.array([2,1,1,2])
    board_dimension_height = 1
    board_dimension_length = 4
    diagonal_connections_allowed = True

    def __init__(self, height = 4, length = 6):
        self.first_player_turn = True
        self.board_dimension_height = height
        self.board_dimension_length = length
        self.pieces = np.zeros((self.board_dimension_height,self.board_dimension_length), dtype = int)
        self.hand1T = 6
        self.hand1O = 6
        self.hand2T = 6
        self.hand2O = 6

    #returns a new State object that is a copy of self
    def state_copy(self):
        copy = State()
        copy.first_player_turn = self.first_player_turn
        copy.pieces = self.pieces.copy()
        copy.hand1T = self.hand1T
        copy.hand1O = self.hand1O
        copy.hand2T = self.hand2T
        copy.hand2O = self.hand2O
        return copy

    #prints the current board with helpful indices on the left and the bottom
    def print_board(self):
        """ Currently just printing the numpy array. """
        for i in range(self.board_dimension_height):
            print(self.pieces[i])

    def board_is_full(self):
        """ Make the entries True if it has a 0 and False if it has 1.
            Then sum up the booleans. If 0, then the board is full. """
        bool_pieces = (self.pieces == 0)
        return bool_pieces.sum() == 0

    #returns the score dictionary for the number of words, toot and otto
    def check_for_words(self):
        # first entry is number of toot's, second is otto's
        score = np.zeros(2, dtype = int)
        for x in range(self.board_dimension_height):
            for y in range(self.board_dimension_length):
                if self.pieces[x,y] != 0:
                    word = None
                    if self.pieces[x,y] == 1:
                        word = State.toot
                        index = 0
                    elif self.pieces[x,y] == 2:
                        word = State.otto
                        index = 1
                    if word is None:
                        continue

                    if self.word_test(x+1, y, word, 1, 0, 1):
                        score[index] += 1
                    if self.word_test(x, y+1, word, 0, 1, 1):
                        score[index] += 1
                    if self.word_test(x+1, y+1, word, 1, 1, 1):
                        score[index] += 1
                    if self.word_test(x+1, y-1, word, 1, -1, 1):
                        score[index] += 1
        return score

    #helper function for checkForWords
    def word_test(self, x, y, word, dx, dy, char_pos_in_word):
        if char_pos_in_word == 4:
            return True
        if x >= self.board_dimension_height or y >= self.board_dimension_length or x < 0 or y < 0:
            return False
        if self.pieces[x,y] != word[char_pos_in_word]:
            return False
        return self.word_test(x+dx, y+dy, word, dx, dy, char_pos_in_word+1)


#Implementation of the neccessary functions for the solver

#assumes that player1 goes for toot and player2 goes for otto

def initial_position():
    return State()

board_state_element_type = MPI.INT

#assumes that if the score is tied, continue playing no matter how many matches
#takes in a state parameter which is a State object
#returns a string of the options win, loss, tie, draw, unkwown

def primitive(state):
    score = state.check_for_words()
    if score[1] >= 1 and score [0] >= 1:
        return 'tie'
    if score[0] >= 1:
        print("toot wins")
        if state.first_player_turn:
            return 'win'
        return 'loss'
    elif score[0] >= 1:
        print("otto wins")
        if state.first_player_turn:
            return 'loss'
        return 'win'
    if state.board_is_full():
        return 'tie'
    else:
        return 'unknown'

#action is defined as a tuple with the letter, and a board location
#example of an action: ("T", (2,3))

#takes in the parameter state, a State object
#returns a list of actions that are valid to be applied to the parameter state
def gen_moves(state):
    hand = np.append(state.hand2T,state.hand2O)
    if state.first_player_turn:
        hand = np.append(state.hand1T,state.hand1O)

    possible_actions = []
    for y in range(State.board_dimension_length):
        x = 0
        while x < State.board_dimension_height and state.pieces[3-x,y] != 0:
            x += 1
        if x < State.board_dimension_height:
            for i in range(2):
                if hand[i]>0:
                    possible_actions.append((i+1, (3-x,y)))
    return possible_actions

#returns the successor given by applying the parameter action to the parameter state
#the parameter action is a tuple with the letter, and a board location
#the parameter state is a State object
#must pass in a valid state and a valid action for that state, does not check
def do_move(state, action):
    successor = state.state_copy()
    piece, loc = action

    successor.first_player_turn = not state.first_player_turn
    successor.pieces[loc] = piece
    if state.first_player_turn and piece == 1:
        successor.hand1T -= 1
    elif state.first_player_turn and piece == 0:
        successor.hand1O -= 1
    elif not state.first_player_turn and piece == 0:
        successor.hand2T -= 1
    else:
        successor.hand2O -= 1
    return successor






#helpful prints for reference, understanding the code, and debugging
def example():
    print('the initial position is the following:')
    initial_position.print_board()
    print('hand1T=' + str(initial_position.hand1T))
    print('hand1O=' + str(initial_position.hand1O))
    print('hand2T=' + str(initial_position.hand2T))
    print('hand2O=' + str(initial_position.hand2O))
    print('firstPlayerTurn=' + str(initial_position.first_player_turn))
    possible_actions = gen_moves(initial_position)
    print('these are the possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(initial_position))

    s = do_move(initial_position, possible_actions[6])
    print('this is the state after a move has been made')
    s.print_board()
    print('hand1T=' + str(s.hand1T))
    print('hand1O=' + str(s.hand1O))
    print('hand2T=' + str(s.hand2T))
    print('hand2O=' + str(s.hand2O))
    print('firstPlayerTurn=' + str(s.first_player_turn))
    possible_actions = gen_moves(s)
    print('New possible actions:')
    print(possible_actions)
    print('primitive value:')
    print(primitive(s))
