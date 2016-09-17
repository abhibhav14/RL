class TicTacToeBoard:
    """Stores a Tic Tac Toe Board

    A TicTacToe Board is a 3x3 matrix laid out as follows:

    * * *
    * * *
    * * *

    """
    board_size = 3
    board_mapping = { 0 : ' ',
                      1 : 'X',
                      2 : 'O' }

    def __init__(self, board_array = None, current_player = 1):
        """Create a new TicTacToeBoard

        If board_array is specified, it thought be a 3x3 array of arrays
        that will be used to describe the initial state

        current_player is the ID of the player who is supposed to make
        the next move
        """
        if board_array == None:
            self._board_array = [[0 for i in range(self.board_size)] for j in range(self.board_size)]
        else:
            self._board_array = list(map(list, board_array))

        self.current_player = current_player

    def get_current_player_id(self):
        """ Returns the id of the player who should be moving now """
        return self.current_player

    def get_other_player_id(self):
        """ Returns the id of the opponent of the player who should be moving now """
        if self.current_player == 1:
            return 2
        return 1

    def get_move_list(self):
        """ Returns a list of possible moves that the current player has available"""
        moves = list()
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self._board_array[i][j] == 0:
                    moves.append([i, j])
        return moves

    def makemove(self, i, j):
        """
        Execute the specified move as the current player.
        Return a new board with the result
        """
        if [i, j] in self.get_move_list():
            new_array = list()
            for p in self._board_array:
                new_array.append(p[:])
            new_array[i][j] = self.get_current_player_id()
            return TicTacToeBoard(new_array, self.get_other_player_id())
        else:
            return 0

    def tie(self):
        """ Returns 1 if the game is tied"""
        for i in self._board_array:
            for j in i:
                if j == 0:
                    return 0
        return 1

    def win(self):
        """ Returns the id of the winner"""
        winner = 0
        if self._board_array[0][0] == self._board_array[0][1] and self._board_array[0][0] == self._board_array[0][2]:
            winner = self._board_array[0][0]
            if winner != 0:
                return winner

        if self._board_array[1][0] == self._board_array[1][1] and self._board_array[1][0] == self._board_array[1][2]:
            winner = self._board_array[1][0]
            if winner != 0:
                return winner

        if self._board_array[2][0] == self._board_array[2][1] and self._board_array[2][0] == self._board_array[2][2]:
            winner = self._board_array[2][0]
            if winner != 0:
                return winner

        if self._board_array[0][0] == self._board_array[1][0] and self._board_array[0][0] == self._board_array[2][0]:
            winner = self._board_array[0][0]
            if winner != 0:
                return winner

        if self._board_array[0][1] == self._board_array[1][1] and self._board_array[0][1] == self._board_array[2][1]:
            winner = self._board_array[0][1]
            if winner != 0:
                return winner

        if self._board_array[0][2] == self._board_array[1][2] and self._board_array[0][2] == self._board_array[2][2]:
            winner = self._board_array[0][2]
            if winner != 0:
                return winner

        if self._board_array[0][0] == self._board_array[1][1] and self._board_array[0][0] == self._board_array[2][2]:
            winner = self._board_array[0][0]
            if winner != 0:
                return winner

        if self._board_array[0][2] == self._board_array[1][1] and self._board_array[0][2] == self._board_array[2][0]:
            winner = self._board_array[0][2]
            if winner != 0:
                return winner

        return winner

    def is_game_over(self):
        """ Returns 1 if the game is over"""
        if self.tie() or self.win():
            return 1
        return 0

    def __str__(self):
        """Returns a formated string representation of the board"""
        s = ""
        for i in self._board_array:
            for j in i:
                s += self.board_mapping[j]
                s += ' '
            s += '\n'
        return s[:-1]



class TicTacToeRunner:
    """
    Runs a game of TicTacToe, using standard rules

    The game runner is implemented via callbacks: The two players specify callbacks
    to be called when it is their turn. The callbacks are called using the board state
    as the argument.

    The callback must return the move they want to make in the form of [row, col]
    """

    def __init__(self, player1_callback, player2_callback, board = TicTacToeBoard()):
        """
        Create a TicTacToeRunner.

        p1cb and p2cb are the callback functions of the two players
        """
        self.p1cb = player1_callback
        self.p2cb = player2_callback
        self.board = board

    def runGame(self, verbose = 1):
        """
        Runs the game of TicTacToe. Returns the id of the winning player

        verbose = 1  : print the game board after every move and the id of the winner
        verbose = 0  : print only the id of the winner at the end
        verbose = -1 : print nothing
        """
        win_for_player = 0
        while not self.board.tie() and not win_for_player:
            for i in [self.p1cb, self.p2cb]:
                if verbose == 1:
                    print('-----------------------')
                    print(self.board)
                    print()
                [newR, newC] = i(self.board)
                self.board = self.board.makemove(newR, newC)
                
                if self.board.is_game_over():
                    win_for_player = self.board.win()
                    break 

        win_for_player = self.board.win()

        if self.board.tie() and not self.board.win():
            if verbose != -1:
                print("It is a tie, game over")
            return 0
        else:
            if verbose != -1:
                print("Player ", end="")
                print(win_for_player, end=" ")
                print("has won")
            return win_for_player
        
    def __str__(self):
        """ Terrible coded bodge, not implemented""" 
        print(self.board)
        return ""
