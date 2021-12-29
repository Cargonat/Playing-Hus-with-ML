import numpy as np


class Game:
    """
    Models a Hus game with board-width 12.
    The active player is always playing in rows 0 and 1,
    i.e. the board flips after every move.
    """

    def __init__(self):
        self.board = self.__init_board__()
        self.turn = 0
        self.log = []

    def __init_board__(self):
        # init board with zeroes
        board = np.zeros((4, 12))
        # we only need 8 bits
        board = board.astype(np.ubyte)

        # initialize board stones
        board[0, :] = 2
        board[1, :6] = 2
        board[2, 6:] = 2
        board[3, :] = 2

        return board

    def move(self, action):
        """
        Plays the given move where 0-11 are the outer row and 12-23 the inner.
        Returns the resulting game, if it is not finished.
        Returns True, if the move was winning, and False if it was losing.
        """

        i, j = action % 12, action // 12
        print(self)

        if not (i, j) in self.legal_actions():
            print(f"Illegal move: {i,j}")
            return False  # lose on illegal moves

        stones = self.board[i, j]
        self.board[i, j] = 0

        while stones != 0:
            print(self)
            i, j = self.__next_pos(i, j)
            if self.board[i, j] > 0 and stones == 1:
                # pick up new stones from field
                stones += self.board[i, j]
                self.board[i, j] = 0

                # check middle row and steal stones
                if i == 1 and self.board[2, j] > 0:
                    stones += self.board[2, j] + self.board[3, j]
                    self.board[2:4, j] = 0
            else:
                # just drop ones stone
                self.board[i, j] += 1
                stones -= 1

        print(self)
        self.turn += 1

        victory = self.check_victory()
        if victory != 0:
            print("You win!" if victory == 1 else "You lose!")

        # flip board for next player
        self.board = self.board[::-1]

        return self

    def __next_pos(self, i, j):
        if i == 0:
            if j != 11:
                return i, j + 1
            else:
                return i + 1, j
        elif i == 1:
            if j != 0:
                return i, j - 1
            else:
                return i - 1, j
        else:
            raise ValueError("Not in row 0 or 1")

    def check_victory(self):
        """
        Checks if the current player has won or lost.
        Returns:
            1,  if current player wins,
            -1, if current player loses,
            0,  otherwise.
        """
        # check oppenent loss then self loss
        for player in [1, 0]:
            half_board = self.board[player * 2 : player * 2 + 2, :]
            loss = all([s < 2 for s in half_board.flatten()])
            if loss:
                return 1 if player == 1 else -1
        return 0

    def legal_actions(self):
        return [(i, j) for i in range(2) for j in range(12) if self.board[i, j] >= 2]

    def __str__(self):
        return str(self.board)
