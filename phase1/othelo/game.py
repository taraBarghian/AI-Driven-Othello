import pygame
from .constants import *
from .piece import *


class Logic:
    def __init__(self):
        self.board_table = []
        self.red_score = self.white_score = 2
        self.remain_pieces = 60
        self.turn = RED_TURN

    def change_Turn(self):
        self.turn = not self.turn

    def opposite_sit(self, color):
        if color == Piece_Situation.RED:
            return Piece_Situation.WHITE
        elif color == Piece_Situation.WHITE:
            return Piece_Situation.RED

    def get_sit_from_turn(self):
        if self.turn == RED_TURN:
            return Piece_Situation.RED
        elif self.turn == WHITE_TURN:
            return Piece_Situation.WHITE

    def set_scores(self, score):
        if self.turn == RED_TURN:
            self.red_score += score + 1
            self.white_score -= score
        elif self.turn == WHITE_TURN:
            self.white_score += score + 1
            self.red_score -= score

    def init(self):
        for row in range(ROWS):
            self.board_table.append([])
            for col in range(COLS):
                if ((row == 3 and col == 3) or (row == 4 and col == 4)):
                    self.board_table[row].append(Piece_Situation.WHITE)
                elif ((row == 4 and col == 3) or (row == 3 and col == 4)):
                    self.board_table[row].append(Piece_Situation.RED)
                else:
                    self.board_table[row].append(Piece_Situation.FREE)

        self.check_choosable_pieces()
        return self.board_table

    def insert(self, ins_row, ins_col):
        self.board_table[ins_row][ins_col] = self.get_sit_from_turn()
        score = self.check_inverses(ins_row, ins_col, self.get_sit_from_turn(),
                                    self.opposite_sit(self.get_sit_from_turn()))
        self.set_scores(score)
        self.change_Turn()
        self.remain_pieces = self.remain_pieces - 1
        if not self.check_choosable_pieces():
            self.change_Turn()
            self.check_choosable_pieces()

        return self.board_table

    def check_end(self):
        return self.remain_pieces <= 0

    def check_inverses(self, row, col, inverter_color, target):
        inverted_pieces = 0

        # left check
        temp_col = col - 1
        while temp_col >= 0 and self.board_table[row][temp_col] == target:
            temp_col = temp_col - 1
        if temp_col >= 0 and self.board_table[row][temp_col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_col != col:
                self.board_table[row][temp_col] = inverter_color
                temp_col = temp_col + 1
                inverted_pieces = inverted_pieces + 1

        # right check
        temp_col = col + 1
        while temp_col < COLS and self.board_table[row][temp_col] == target:
            temp_col = temp_col + 1
        if temp_col < COLS and self.board_table[row][temp_col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_col != col:
                self.board_table[row][temp_col] = inverter_color
                temp_col = temp_col - 1
                inverted_pieces = inverted_pieces + 1

        # up check
        temp_row = row - 1
        while temp_row >= 0 and self.board_table[temp_row][col] == target:
            temp_row = temp_row - 1
        if temp_row >= 0 and self.board_table[temp_row][col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_row != row:
                self.board_table[temp_row][col] = inverter_color
                temp_row = temp_row + 1
                inverted_pieces = inverted_pieces + 1

        # down check
        temp_row = row + 1
        while temp_row < ROWS and self.board_table[temp_row][col] == target:
            temp_row = temp_row + 1
        if temp_row < ROWS and self.board_table[temp_row][col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_row != row:
                self.board_table[temp_row][col] = inverter_color
                temp_row = temp_row - 1
                inverted_pieces = inverted_pieces + 1

        # DOWN-RIGHT check
        temp_col = col + 1
        temp_row = row + 1
        while temp_col < COLS and temp_row < ROWS and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col + 1
            temp_row = temp_row + 1
        if temp_col < COLS and temp_row < ROWS and self.board_table[temp_row][temp_col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_col != col:
                self.board_table[temp_row][temp_col] = inverter_color
                temp_col = temp_col - 1
                temp_row = temp_row - 1
                inverted_pieces = inverted_pieces + 1

        # UP-RIGHT check
        temp_col = col + 1
        temp_row = row - 1
        while temp_col < COLS and temp_row >= 0 and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col + 1
            temp_row = temp_row - 1
        if temp_col < COLS and temp_row >= 0 and self.board_table[temp_row][temp_col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_col != col:
                self.board_table[temp_row][temp_col] = inverter_color
                temp_col = temp_col - 1
                temp_row = temp_row + 1
                inverted_pieces = inverted_pieces + 1

        # UP-LEFT check
        temp_col = col - 1
        temp_row = row - 1
        while temp_col >= 0 and temp_row >= 0 and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col - 1
            temp_row = temp_row - 1
        if temp_col >= 0 and temp_row >= 0 and self.board_table[temp_row][temp_col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_col != col:
                self.board_table[temp_row][temp_col] = inverter_color
                temp_col = temp_col + 1
                temp_row = temp_row + 1
                inverted_pieces = inverted_pieces + 1

        # DOWN-LEFT check
        temp_col = col - 1
        temp_row = row + 1
        while temp_col >= 0 and temp_row < ROWS and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col - 1
            temp_row = temp_row + 1
        if temp_col >= 0 and temp_row < ROWS and self.board_table[temp_row][temp_col] == inverter_color:
            inverted_pieces = inverted_pieces - 1
            while temp_col != col:
                self.board_table[temp_row][temp_col] = inverter_color
                temp_col = temp_col + 1
                temp_row = temp_row - 1
                inverted_pieces = inverted_pieces + 1

        return inverted_pieces

    def check_choosable_pieces(self):
        is_there_any_choosable_piece = False
        for row in range(ROWS):
            for col in range(COLS):
                if self.board_table[row][col] == Piece_Situation.CHOOSABLE:
                    self.board_table[row][col] = Piece_Situation.FREE
                if self.board_table[row][col] == Piece_Situation.FREE and \
                        self.is_choosable(row, col, self.get_sit_from_turn(),
                                          self.opposite_sit(self.get_sit_from_turn())):
                    is_there_any_choosable_piece = True
                    self.board_table[row][col] = Piece_Situation.CHOOSABLE

        return is_there_any_choosable_piece

    def is_choosable(self, row, col, inverter_color, target):

        # left check
        temp_col = col - 1
        while temp_col >= 0 and self.board_table[row][temp_col] == target:
            temp_col = temp_col - 1
        if temp_col >= 0 and self.board_table[row][temp_col] == inverter_color and temp_col != col - 1:
            return True

        # right check
        temp_col = col + 1
        while temp_col < COLS and self.board_table[row][temp_col] == target:
            temp_col = temp_col + 1
        if temp_col < COLS and self.board_table[row][temp_col] == inverter_color and temp_col != col + 1:
            return True

        # up check
        temp_row = row - 1
        while temp_row >= 0 and self.board_table[temp_row][col] == target:
            temp_row = temp_row - 1
        if temp_row >= 0 and self.board_table[temp_row][col] == inverter_color and temp_row != row - 1:
            return True

        # down check
        temp_row = row + 1
        while temp_row < ROWS and self.board_table[temp_row][col] == target:
            temp_row = temp_row + 1
        if temp_row < ROWS and self.board_table[temp_row][col] == inverter_color and temp_row != row + 1:
            return True

        # DOWN-RIGHT check
        temp_col = col + 1
        temp_row = row + 1
        while temp_col < COLS and temp_row < ROWS and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col + 1
            temp_row = temp_row + 1
        if temp_col < COLS and temp_row < ROWS and self.board_table[temp_row][
            temp_col] == inverter_color and temp_row != row + 1:
            return True

        # UP-RIGHT check
        temp_col = col + 1
        temp_row = row - 1
        while temp_col < COLS and temp_row >= 0 and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col + 1
            temp_row = temp_row - 1
        if temp_col < COLS and temp_row >= 0 and self.board_table[temp_row][
            temp_col] == inverter_color and temp_row != row - 1:
            return True

        # UP-LEFT check
        temp_col = col - 1
        temp_row = row - 1
        while temp_col >= 0 and temp_row >= 0 and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col - 1
            temp_row = temp_row - 1
        if temp_col >= 0 and temp_row >= 0 and self.board_table[temp_row][
            temp_col] == inverter_color and temp_row != row - 1:
            return True

        # DOWN-LEFT check
        temp_col = col - 1
        temp_row = row + 1
        while temp_col >= 0 and temp_row < ROWS and self.board_table[temp_row][temp_col] == target:
            temp_col = temp_col - 1
            temp_row = temp_row + 1
        if temp_col >= 0 and temp_row < ROWS and self.board_table[temp_row][
           temp_col] == inverter_color and temp_row != row + 1:
            return True

        return False

    def get_status(self):
        return {
            "white_score": self.white_score,
            "red_score": self.red_score,
            "remain_pieces": self.remain_pieces,
            "turn": "red" if self.turn == RED_TURN else "white"
        }
