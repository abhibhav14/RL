import tictactoe as t
import random
import matplotlib.pyplot as plt

class Agent(object):
    """Agent for Reinforcement Tic Tac Toe
    """
    def __init__(self, player, rate=0.99, eps=0.1, lossval=0, learning=False):
        #Stores all the params of the learning Agent

        self.data = dict()
        self.player = player
        self.rate = rate
        self.eps = eps
        self.lossval = lossval
        self.learning =  learning
        self.prev_move = None

    def trainer(self, games, opponent):
        #AI to train the agent
        
        winP = list()
        wins = 0.0
        tempLearnMode = self.learning
        self.learning = True
        self.prev_move = None
        print('Training...')
        for i in range(games):
            game = t.TicTacToeRunner(self.callback, opponent)
            winner = game.runGame(verbose=-1)
            if (winner == 3 - self.player):
                score = self.lossval
                old = self.data[self.prev_move]
                self.data[self.prev_move] = old + self.rate * (score - old)
            self.prev_move = None
            if winner == self.player:
                wins += 1

            winP.append(wins / (i + 1))

        self.learning = tempLearnMode
        return winP
        

    def callback(self, board):
        #Main callback function, decides moves and calls appropriate function
        moveList = board.get_move_list()
        bestVal = [None, None]
        r = random.random()
        
        if r < self.eps:
            m = random.choice(moveList)
            self.playedRandom(board, m)
            return m[:]
        
        else:
            for i in moveList:
                value = self.lookup(board.makemove(*i))
                if bestVal[0] == None or value > bestVal[0]:
                    bestVal[0] = value
                    bestVal[1] = i[:]
            m = bestVal[1][:]
            self.playedGreedy(board, m)
            return m[:]

    def playedRandom(self, board, m):
        #If played randomly, just update previous move
        
        movekey = self.makeKey(board, m)
        self.prev_move = movekey
        if not movekey in self.data:
            self.add(board.makemove(*m))

    def playedGreedy(self, board, m):
        #If played greedily, learn from it
        
        movekey = self.makeKey(board, m)
        if self.prev_move:
            old = self.data[self.prev_move]
            if self.learning:
                self.data[self.prev_move] = old + self.rate * (self.data[movekey] - old)
        self.prev_move = movekey

    def lookup(self, board):
        #looks up scores and returns them
        key = self.makeKey(board)
        if not key in self.data:
            self.add(board)
        return self.data[key]

    def add(self, board):
        key = self.makeKey(board)
        self.data[key] = self.score(board)

    def score(self, board):
        #Scores a board and adds the key
        
        if not board.is_game_over():
            return 0.5

        if board.win() == self.player:
            return 1

        if board.tie():
            return 0

        return self.lossval

    def makeKey(self, board, m=None):
        #Take a board and a move, and output key after the move made
        key = ''
        for i in board._board_array:
            for j in i:
                key += str(j)
        if m == None:
            return key
        pos = m[0] * 3 + m[1]
        key = key[:pos] + str(self.player) + key[pos + 1:]
        return key


def randomMove(board):
    a = random.choice(board.get_move_list())
    return a

a = Agent(1)
data = a.trainer(10000, randomMove)
print('Plot:')
plt.plot(data)
plt.show()
