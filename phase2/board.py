from config import *
from copy import deepcopy
import numpy as np


class Board:

    def __init__(self):
        self.board = np.zeros((8, 8), dtype=np.integer)
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[3][3] = WHITE
        self.board[4][4] = WHITE
        self.valid_moves = []
        self.best_valid_moves = []

    def __getitem__(self, i, j):
        return self.board[i][j]

    # return the possible positions exist
    def find_all_dirs(self, row, col, color):
        if color == BLACK:
            other = WHITE
        else:
            other = BLACK
        dirs = [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1)
        ]
        places = []
        if row < 0 or row > 7 or col < 0 or col > 7:
            return places

        # check all directions for possible moves
        for (x, y) in dirs:
            pos = self.check_direction(row, col, x, y, other)
            if pos:
                places.append(pos)
        return places

    def check_direction(self, row, column, row_add, column_add, other_color):
        i = row + row_add
        j = column + column_add
        if (i >= 0 and j >= 0 and i <= 7 and j <= 7 and self.board[i][j] == other_color):
            i += row_add
            j += column_add
            while (i >= 0 and j >= 0 and i <= 7 and j <= 7 and self.board[i][j] == other_color):
                i += row_add
                j += column_add
            if (i >= 0 and j >= 0 and i <= 7 and j <= 7 and self.board[i][j] == EMPTY):
                return (i, j)

    def get_valid_moves(self, color):

        places = []

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    places = places + self.find_all_dirs(i, j, color)

        #places = self.logic_filter(places)
        # make it unique
        places = list(set(places))
        self.valid_moves = places
        #self.get_best_valid_moves(color)
        return places

    def get_best_valid_moves(self, color):
        bestie = self.get_valid_moves(color)
        self.best_valid_moves=self.logic_filter(bestie)
        return self.best_valid_moves

    def logic_filter(self, places):
        weights = [
            [100, -20, 10, 5, 5, 10, -20, 100],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [5, -2, -1, -1, -1, -1, -2, 5],
            [10, -2, -1, -1, -1, -1, -2, 10],
            [-20, -50, -2, -2, -2, -2, -50, -20],
            [100, -20, 10, 5, 5, 10, -20, 100],
        ]


        if len(places) < 5:
            deleted_item = int(0.3 * len(places))
        elif len(places) < 10:
            deleted_item = int(0.6 * len(places))
        elif len(places) < 14:
            deleted_item = int(0.7 * len(places))
        elif len(places) < 17:
            deleted_item = int(0.8 * len(places))
        else:
            deleted_item = int(0.9 * len(places))

        best_places = [(x, weights[x[0]][x[1]]) for x in places]
        best_places = sorted(best_places, key= lambda x:x[1])
        best_places = best_places[deleted_item:]
        best_places = [x[0] for x in best_places]
        return best_places


    # check if the move is correct then apply it and change the board.
    def apply_move(self, move, color):
        if move in self.valid_moves:
            self.board[move[0]][move[1]] = color
            for i in range(1, 9):
                self.flip(i, move, color)

    def flip(self, direction, position, color):
        if color == WHITE:
            other = BLACK
        else:
            other = WHITE

        switcher = {
            1: (-1, 0),
            2: (-1, 1),
            3: (0, 1),
            4: (1, 1),
            5: (1, 0),
            6: (1, -1),
            7: (0, -1),
            8: (-1, -1)
        }

        inc = switcher.get(direction)
        i = position[0] + inc[0]
        j = position[1] + inc[1]
        places = []

        if i in range(8) and j in range(8) and self.board[i][j] == other:
            # assures there is at least one piece to flip
            places = places + [(i, j)]
            i = i + inc[0]
            j = j + inc[1]
            while i in range(8) and j in range(8) and self.board[i][j] == other:
                # search for more pieces to flip
                places = places + [(i, j)]
                i = i + inc[0]
                j = j + inc[1]
            if i in range(8) and j in range(8) and self.board[i][j] == color:
                # found a piece of the right color to flip the pieces between
                for pos in places:
                    # flips
                    self.board[pos[0]][pos[1]] = color

    def get_changes(self):
        whites = 0
        blacks = 0
        empty = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == WHITE:
                    whites += 1
                elif self.board[i][j] == BLACK:
                    blacks += 1
                else:
                    empty += 1
        return whites, blacks, empty

    def game_ended(self):
        # board full or no move exists
        whites, blacks, empty = self.get_changes()
        if whites == 0 or blacks == 0 or empty == 0:
            return True

        # no valid moves for both players
        # todo print it
        if self.get_valid_moves(BLACK) == [] and self.get_valid_moves(WHITE) == []:
            return True

        return False

    # return empties we can use
    def get_adjacent_count(self, color):
        adjCount = 0
        for x, y in [(a, b) for a in range(8) for b in range(8) if self.board[a][b] == color]:
            for i, j in [(a, b) for a in [-1, 0, 1] for b in [-1, 0, 1]]:
                if 0 <= x + i <= 7 and 0 <= y + j <= 7:
                    if self.board[x + i][y + j] == EMPTY:
                        adjCount += 1
        return adjCount

    # using to get best moves for minimax
    def next_states(self, color):
        # iterator
        valid_moves = self.get_best_valid_moves(color)
        for move in valid_moves:
            newBoard = deepcopy(self)
            newBoard.apply_move(move, color)
            yield newBoard

    def compare(self, otherBoard):

        # return just different pos (empty)
        diffBoard = Board()
        diffBoard.board[3][4] = 0
        diffBoard.board[3][3] = 0
        diffBoard.board[4][3] = 0
        diffBoard.board[4][4] = 0
        for i in range(8):
            for j in range(8):
                if otherBoard.board[i][j] != self.board[i][j]:
                    diffBoard.board[i][j] = otherBoard.board[i][j]
        return otherBoard
