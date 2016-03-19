import gamesman
import numpy as np

#Toot and Otto game implementation for Gamescrafters

LOSS, WIN, TIE, DRAW, UNDECIDED = "LOSS", "WIN", "TIE", "DRAW", "UNDECIDED"

toot = np.array([1,2,2,1])
otto = np.array([2,1,1,2])

height = 4
length = 6

initial_position = np.zeros((height+1,length), dtype = np.int8)
# top row is number of T for P1, O for P1, T for P2, O for P3, 
# which player is toot, and the first player
initial_position[0,] = [6, 6, 6, 6, 1, 1]

def print_board(board):
	#prints the current board with helpful indices on the left and the bottom
	for i in range(1,height+1):
		print board[i]

# def board_is_full(board):
# 	bool_pieces = (board[1:height+1,]  == 0)
# 	return bool_pieces.sum() == 0

def board_is_full(board):
	return np.count_nonzero(board[1:height+1,:]) == height*length

def check_for_words(board):
	# first entry is number of toot's, second is otto's
	score = np.zeros(2, dtype = np.int8)
	for x in range(1,height+1):
		for y in range(length):
			if board[x,y] != 0:
				word = None
				if board[x,y] == 1:
					word = toot
					index = 0
				elif board[x,y] == 2:
					word = otto
					index = 1
				if word is None:
					continue

				if word_test(board, x+1, y, word, 1, 0, 1):
					score[index] += 1
				if word_test(board, x, y+1, word, 0, 1, 1):
					score[index] += 1
				if word_test(board, x+1, y+1, word, 1, 1, 1):
					score[index] += 1
				if word_test(board, x+1, y-1, word, 1, -1, 1):
					score[index] += 1
	return score

def word_test(board, x, y, word, dx, dy, char_pos_in_word):
	if char_pos_in_word == 4:
		return True
	if x >= height+1 or y >= length or x < 1 or y < 0:
		return False
	if board[x,y] != word[char_pos_in_word]:
		return False
	return word_test(board, x+dx, y+dy, word, dx, dy, char_pos_in_word+1)

#Implementation of the neccessary functions for the solver

#assumes that player1 goes for toot and player2 goes for otto

#assumes that if the score is tied, continue playing no matter how many matches
#takes in a state parameter which is a State object
#returns a string of the options win, loss, tie, draw, unkwown

def primitive(board):
	score = check_for_words(board)
	if score[1] >= 1 and score[0] >= 1:
		return TIE
	if score[0] >= 1:
		print("toot wins")
		if board[0,5] == 1:
			return WIN
		return LOSS
	elif score[0] >= 1:
		print("otto wins")
		if board[0,5] == 1:
			return LOSS
		return WIN
	if board_is_full(board):
		return TIE
	else:
		return UNDECIDED

#action is defined as a tuple with the letter, and a board location
#example of an action: ("T", (2,3))

#takes in the parameter state, a State object
#returns a list of actions that are valid to be applied to the parameter state
def gen_moves(board):
	hand = np.append(board[0,2],board[0,3])
	if board[0,4] == 1:
		hand = np.append(board[0,0],board[0,1])

	possible_actions = []
	for y in range(6):
		x = 0
		while x < 4 and board[4-x,y] != 0:
			x += 1
		if x < 4:
			for i in range(2):
				if hand[i]>0:
					possible_actions.append((i+1, (4-x,y)))

	return possible_actions

#returns the successor given by applying the parameter action to the parameter state
#the parameter action is a tuple with the letter, and a board location
#the parameter state is a State object
#must pass in a valid state and a valid action for that state, does not check
def do_move(board, action):
	valid_moves = gen_moves(board)
	if action not in valid_moves:
		print 'INVALID MOVE'
		return board

	piece, loc = action

	board[loc] = piece
	if board[0,4]==1 and piece == 1:
		board[0,0] -= 1
	elif board[0,4]==1 and piece == 2:
		board[0,1] -= 1
	elif board[0,4]==2 and piece == 1:
		board[0,2] -= 1
	else:
		board[0,3] -= 1

	board[0,4] = 1 + (board[0,4] % 2)

	return board


#helpful prints for reference, understanding the code, and debugging
def example():
	print 'the initial position is the following:'
	print_board(initial_position)
	print 'hand1T=' + str(initial_position[0,0])
	print 'hand1O=' + str(initial_position[0,1])
	print 'hand2T=' + str(initial_position[0,2])
	print 'hand2O=' + str(initial_position[0,3])
	print 'firstPlayerTurn=' + str(initial_position[0,4]==1)
	possible_actions = gen_moves(initial_position)
	print 'these are the possible actions:'
	print possible_actions
	print 'primitive value:'
	print primitive(initial_position)

	board_turn_1 = do_move(initial_position, possible_actions[6])
	print 'this is the state after a move has been made'
	print_board(board_turn_1)
	print 'hand1T=' + str(board_turn_1[0,0])
	print 'hand1O=' + str(board_turn_1[0,1])
	print 'hand2T=' + str(board_turn_1[0,2])
	print 'hand2O=' + str(board_turn_1[0,3])
	print 'firstPlayerTurn=' + str(board_turn_1[0,4]==1)
	possible_actions = gen_moves(board_turn_1)
	print 'New possible actions:'
	print possible_actions
	print 'primitive value:'
	print primitive(board_turn_1)

	board = do_move(board_turn_1, possible_actions[4])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions:'
	print possible_actions
	print 'primitive value:'
	print primitive(board)

	board = do_move(board, possible_actions[4])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions length:'
	print len(possible_actions)
	print 'primitive value:'
	print primitive(board)

	board = do_move(board, possible_actions[4])
	print 'this is the state after a move has been made'
	print_board(board)
	print 'hand1T=' + str(board[0,0])
	print 'hand1O=' + str(board[0,1])
	print 'hand2T=' + str(board[0,2])
	print 'hand2O=' + str(board[0,3])
	print 'firstPlayerTurn=' + str(board[0,4]==1)
	possible_actions = gen_moves(board)
	print 'New possible actions length:'
	print len(possible_actions)
	print 'primitive value:'
	print primitive(board)




