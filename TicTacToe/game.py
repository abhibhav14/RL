import tictactoe as t
import random
import pickle

with open('memory.pickle', 'rb') as handle:
    AImem = pickle.load(handle)

#user input function
def human(board):
    print("It is the turn of player:", end=' ')
    print(board.get_current_player_id())
    print("Moves available:")
    print(board.get_move_list())
    a, b = map(int, input("Enter Move:").split())
    return [a, b]

#minimax
def minimax_helper(board, alpha, beta):
    if board.tie():
        return 0
    if board.win() == board.get_current_player_id():
        return 10
    if board.win() == board.get_other_player_id():
        return -10

    bestVal = None
    for i in board.get_move_list():
        curr_val = -1 * minimax_helper(board.makemove(*i), -beta, -alpha)
        if bestVal == None or bestVal < curr_val:
            bestVal = curr_val
            alpha = curr_val
            if beta <= alpha:
                break

    return bestVal
def minimax(board):
    bestVal = None
    alpha = -1000000
    beta = 1000000
    for i in board.get_move_list():
        curr_val = -1 * minimax_helper(board.makemove(*i), -beta, -alpha)
        if bestVal == None or bestVal[0] < curr_val:
            bestVal = [curr_val, i[:]]
            alpha = curr_val
    return bestVal[1]

#random
def randomMove(board):
    a =  random.choice(board.get_move_list())
    return a

#using AI
def AI(board):
    boardKey = ''
    for i in board._board_array:
        for j in i:
            boardKey += str(j)
    bestVal = None
    player = board.get_current_player_id()
    for i in board.get_move_list():
        newKey = str()
        moveMade = i[0] * 3 + i[1]
        newKey = boardKey[:moveMade] + str(player) + boardKey[moveMade + 1:]
        curr_val = 0
        if newKey in AImem.keys():
            curr_val = AImem[newKey]
        # print(i, end = ':')
        # print(curr_val)
        if bestVal == None or bestVal[0] < curr_val:
            bestVal = [curr_val, i]
    # print('----Move Done----')
    return bestVal[1]

#Create a TicTacToe Game Runner object with a callback for each player
#Current available callbacks:
# 1. human
# 2. minimax (needs work)
# 3. randomMove
# 4. AI (using trained AI)
A = t.TicTacToeRunner(AI, human)
A.runGame(verbose=1)
