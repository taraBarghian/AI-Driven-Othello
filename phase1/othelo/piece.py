from .constants import *
import pygame
from enum import Enum


class Piece_Situation(Enum):
    WHITE = 1
    RED = 2
    CHOOSABLE = 3
    FREE = 4

#Piece class could be removed

class Piece:

    def __init__(self):
        self.row = 0
        self.col = 0
        self.color = 0

        # self.selected = False

        self.x = 0
        self.y = 0

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win, row, col, piece_sit):
        # self.color = color
        self.row = row
        self.col = col
        self.calc_pos()
        radius = SQUARE_SIZE // 2 - PADDING
        if piece_sit == Piece_Situation.WHITE:
            pygame.draw.circle(win, BLACK, (self.x, self.y), radius + OUTLINE)
            pygame.draw.circle(win, WHITE, (self.x, self.y), radius)
        elif piece_sit == Piece_Situation.RED:
            pygame.draw.circle(win, BLACK, (self.x, self.y), radius + OUTLINE)
            pygame.draw.circle(win, RED, (self.x, self.y), radius)
        elif piece_sit == Piece_Situation.CHOOSABLE:
            pygame.draw.circle(win, DARK, (self.x, self.y), radius - OUTLINE)
            pygame.draw.circle(win, LIGHTPINK1, (self.x, self.y), radius - 2 * OUTLINE)
            pygame.draw.circle(win, LIGHTPINK2, (self.x, self.y), radius - 3 * OUTLINE)
            pygame.draw.circle(win, LIGHTPINK3, (self.x, self.y), radius - 4 * OUTLINE)
            pygame.draw.circle(win, LIGHTPINK4, (self.x, self.y), radius - 5 * OUTLINE)
