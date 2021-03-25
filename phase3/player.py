from config import *
import random
from evaluator import Evaluator
from minimax import Minimax


def change_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK


class Human:

    def __init__(self, gui, color="black"):
        self.color = color
        self.gui = gui

    def get_move(self):
        validMoves = self.current_board.get_valid_moves(self.color)
        while True:
            move = self.gui.get_mouse_input()
            if move in validMoves:
                break
        self.current_board.apply_move(move, self.color)
        return 0, self.current_board

    def get_current_board(self, board):
        self.current_board = board


class Computer(object):

    def __init__(self, color, depth=5,vec=None):
        self.depthLimit = depth
        evaluator = Evaluator(vec)
        self.minimaxObj = Minimax(evaluator.evaluate_all_heuristics)
        self.color = color

    def get_current_board(self, board):
        self.current_board = board

    def get_move(self):
        return self.minimaxObj.minimax(self.current_board, None, self.depthLimit, self.color,
                                       change_color(self.color))

