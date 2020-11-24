import pygame
from .constants import *
from .game import *
from .piece import Piece


class Board:
    INFO_PADDING = 5
    PIECE_PADDING = WIDTH // 12
    R = 13
    PIECE_OUTLINE = 15

    def __init__(self):
        self.logic = Logic()
        self.board = self.logic.init()
        self.selected_piece = None
        self.white_left = self.black_left = 64
        self.ischoosable = 0
        # self.red_kings = ??

    def draw_cubes(self, win):
        win.fill(GREEN)
        # for row in range(ROWS):
        #     for col in range(row % 2, ROWS, 2):
        #         pygame.draw.rect(win, BLUE, (row * SQUARE_SIZE, col * SQUARE_SIZE,
        #                                      SQUARE_SIZE, SQUARE_SIZE))
        boardImg = pygame.image.load('othelo/assets/board.jpg')
        boardImg = pygame.transform.scale(boardImg, (BOARD_WIDTH, BOARD_HEIGHT))
        win.blit(boardImg, (0, 0))
        self.show_info(win)

    def show_info(self, win):
        # boarder :
        pygame.draw.rect(win, GRAY, (0, BOARD_HEIGHT,
                                     WIDTH, HEIGHT - BOARD_HEIGHT))
        boardImg = pygame.image.load('othelo/assets/billboard.jpg')
        boardImg = pygame.transform.scale(boardImg, (BOARD_WIDTH + self.INFO_PADDING, HEIGHT - BOARD_HEIGHT))
        win.blit(boardImg, (-self.INFO_PADDING, BOARD_HEIGHT + self.INFO_PADDING))

        # point & turn :

        pygame.draw.circle(win, BLACK, (self.PIECE_PADDING * 3, HEIGHT - 2 * self.PIECE_PADDING), self.PIECE_OUTLINE)
        pygame.draw.circle(win, RED, (self.PIECE_PADDING * 3, HEIGHT - 2 * self.PIECE_PADDING), self.R)

        pygame.draw.circle(win, BLACK, (self.PIECE_PADDING * 3, HEIGHT - 0.8 * self.PIECE_PADDING), self.PIECE_OUTLINE)
        pygame.draw.circle(win, WHITE, (self.PIECE_PADDING * 3, HEIGHT - 0.8 * self.PIECE_PADDING), self.R)

    def get_status(self):
        status = self.logic.get_status()

    def insert(self, row, col, win):
        # check where clicked? shuold be in choosable places
        self.ischoosable = 0
        if self.board[row][col] == Piece_Situation.CHOOSABLE:
            self.board = self.logic.insert(row, col)
            print("red: ", self.logic.red_score, " white: ", self.logic.white_score)
        elif self.board[row][col] == Piece_Situation.WHITE or self.board[row][col] == Piece_Situation.RED:
            print("error you cant invert this piece")
            self.ischoosable = 1

        else:
            print("error please choose a legal place")
            self.ischoosable = 2

    def show_err_score(self, win):

        self.show_info(win)
        turn = MYFONT.render(str("Turn : " + self.logic.get_status()['turn']), True, WHITE)
        win.blit(turn, (self.PIECE_PADDING * 6, HEIGHT - (2.2 * self.PIECE_PADDING)))
        red_scoretext = MYFONT.render(str(self.logic.red_score), True, WHITE)
        win.blit(red_scoretext, (self.PIECE_PADDING * 4, HEIGHT - (2.2 * self.PIECE_PADDING)))
        white_scoretext = MYFONT.render(str(self.logic.white_score), True, WHITE)
        win.blit(white_scoretext, (self.PIECE_PADDING * 4, HEIGHT - self.PIECE_PADDING))

        if (self.ischoosable == 1):
            check = MYFONT.render(str("you cant invert this piece"), True, WHITE)
            win.blit(check, (self.PIECE_PADDING * 5, HEIGHT - (1.5 * self.PIECE_PADDING)))
        elif (self.ischoosable == 2):
            check = MYFONT.render(str("please choose a legal place"), True, WHITE)
            win.blit(check, (self.PIECE_PADDING * 5, HEIGHT - (1.5 * self.PIECE_PADDING)))

    def draw(self, win):
        self.draw_cubes(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece_sit = self.board[row][col]
                piece = Piece()
                piece.draw(win, row, col, piece_sit)

        self.show_err_score(win)

        if self.logic.check_end():
            print("end")
            return "end"

    def draw_end_game(self, win):
        pygame.draw.rect(win, ENDPAGECOLOR, (2 * SQUARE_SIZE, 2 * SQUARE_SIZE,
                                             SQUARE_SIZE * 4, SQUARE_SIZE * 4))

        end = pygame.image.load('othelo/assets/end.png')
        end = pygame.transform.scale(end, (4 * SQUARE_SIZE, 4 * SQUARE_SIZE))
        win.blit(end, (2 * SQUARE_SIZE, 2 * SQUARE_SIZE))

        # show winner and scores
        # show buutonsfor  1.restart , 2.end

    def check_position_in_end_page(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE

        if (row == 2 or row == 3):
            if col == 2 or col == 3:
                return "quit"
            elif col == 4 or col == 5:
                return "restart"
        # return value could be "quit" or "restart"
