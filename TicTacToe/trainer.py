import tictactoe as t
import random
import pickle
"""If AI already has memory append to that otherwise start fresh"""
try:
    with open('memory.pickle', 'rb') as handle:
        learner = pickle.load(handle)
except FileNotFoundError:
    learner = dict()

movelist = list()

def randomMove(board):
    """Generate random move and store moves made in movelist to be used later"""
    a =  random.choice(board.get_move_list())
    movelist.append(a[:])
    return a

def trainer():
    """
    Function that actually trains the AI by watching two people
    play at complete random. Based on the outcome, positive scores
    are given to the moves made by the winning player depending
    on how fast it won, the faster the better.

    The memory of the AI is a dictionary with keys representing game
    states as string of length nine, consisting of digits 0, 1, 2
    depending on the piece at each state.

    Each state is given a score with respect to the last player that
    played, for example 000010000 is how good it is for the first player
    to play in the centre, while 200010000 is how good it is for the
    second player to respond to the  centre move with a top left corner
    move.

    After the learning is complete, when it is the turn of the AI, all
    possible game states are calculated that can be achieved with that
    move, and the one with the best score is picked.
    """

    print('Training...')
    global movelist
    #Learn from a fixed number of games, one per loop
    for i in range(50000):
        #Run a game with random players and get info about it
        A = t.TicTacToeRunner(randomMove, randomMove)
        w = A.runGame(verbose=-1)
        key = "000000000" 
        turn = 0
        score = 15 - len(movelist)
        # For every move made, learn from it.
        # If the first player won, reward his moves and punish player 2
        # If the second player won, reward his moves and punish player 1
        for i in range(len(movelist)):
            if i % 2 == 0:
                # Moves made by first player
                moveMade = movelist[i][0] * 3 + movelist[i][1]
                key = key[:moveMade] + '1' + key[moveMade + 1:]
                try:
                    # If player 1 was winner reward him, else punish him
                    if w == 1: 
                        learner[key] += (score / 100)
                    elif w == 2:
                        learner[key] -= (score / 100)
                except:
                    if w == 1:
                        learner[key] = (score / 100)
                    elif w == 2:
                        learner[key] = -(score / 100)
            else:
                # Moves made by second player
                moveMade = movelist[i][0] * 3 + movelist[i][1]
                key = key[:moveMade] + '2' + key[moveMade + 1:]
                try:
                    # If player 2 was winner reward him, else punish him
                    if w == 2: 
                        learner[key] += ((score) / 100) 
                    elif w == 1:
                        learner[key] -= ((score) / 100)
                except:
                    if w == 2:
                        learner[key] = ((score) / 100)
                    elif w == 1:
                        learner[key] = -((score) / 100)
                # Later moves are more rewarded/penalized
                score += 2
        movelist = list()

# For training the AI and dumping what is has learnt into a file
trainer()
with open('memory.pickle', 'wb') as handle:
    pickle.dump(learner, handle)
