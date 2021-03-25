import pygame
import sys
from pygame.locals import *
import time
from config import *
import pygame_menu
import os
import logging

logger = logging.getLogger('root')


class Gui:
    def __init__(self):

        pygame.init()

        # colors
        self.BACK_GR = (219, 206, 176)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.YELLOW = (239, 239, 176)

        self.BACKGROUND = (219, 206, 176)

        # display
        self.SCREEN_SIZE = (640, 480)
        self.BOARD_POS = (100, 20)
        self.BOARD = (120, 40)
        self.BOARD_SIZE = 400
        self.SQUARE_SIZE = 50
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        # messages
        self.BLACK_LAB_POS = (5, self.SCREEN_SIZE[1] / 4)
        self.WHITE_LAB_POS = (560, self.SCREEN_SIZE[1] / 4)
        self.font = pygame.font.SysFont("Times New Roman", 22)
        self.scoreFont = pygame.font.SysFont("Serif", 58)

        # image files
        self.board_img = pygame.image.load(os.path.join(
            "assets", "board.bmp")).convert()
        self.black_img = pygame.image.load(os.path.join(
            "assets", "black.bmp")).convert()
        self.white_img = pygame.image.load(os.path.join(
            "assets", "white.bmp")).convert()
        self.tip_img = pygame.image.load(os.path.join("assets",
                                                      "tip.bmp")).convert()
        self.clear_img = pygame.image.load(os.path.join("assets",
                                                        "empty.bmp")).convert()

    def show_menu(self, start_cb):
        # default game settings

        self.player1 = HUMAN
        self.player2 = COMPUTER

        self.menu = pygame_menu.Menu(300, 400, 'Othello',
                                     theme=pygame_menu.themes.THEME_ORANGE)
        self.menu.add_button('Play', lambda: start_cb(self.player1, self.player2))

        self.menu.add_selector('First player', [[HUMAN, 1], [COMPUTER, 2]],
                               onchange=self.set_player_1)
        self.menu.add_selector('Second player', [[COMPUTER, 2], [HUMAN, 1]],
                               onchange=self.set_player_2)
        self.menu.mainloop(self.screen)

    def set_player_1(self, value, player):
        logger.debug('value:%s, player:%s', value, player)
        self.player1 = [0, HUMAN, COMPUTER][player]

    def set_player_2(self, value, player):
        logger.debug('value:%s, player:%s', value, player)
        self.player2 = [0, HUMAN, COMPUTER][player]

    def reset_menu(self):
        self.menu.disable()
        self.menu.reset(1)

    def show_winner(self, player_color):
        self.screen.fill(pygame.Color(219, 206, 176, 50))
        font = pygame.font.SysFont("Courier New", 34)
        if player_color == BLACK:
            msg = font.render("Black player wins \n Do you want to play again?", True, self.BLACK)
        elif player_color == WHITE:
            msg = font.render("White player wins \n Do you want to play again?", True, self.BLACK)
        else:
            msg = font.render("Tie ! \n Do you want to play again?", True, self.BLACK)

        time.sleep(2)
        self.screen.blit(
            msg, msg.get_rect(
                centerx=self.screen.get_width() / 2, centery=120))
        pygame.display.flip()

    def show_game(self):

        self.reset_menu()

        # draws screen
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill(self.BACKGROUND)
        self.score_size = 50
        self.score1 = pygame.Surface((self.score_size, self.score_size))
        self.score2 = pygame.Surface((self.score_size, self.score_size))
        self.screen.blit(self.background, (0, 0), self.background.get_rect())
        self.screen.blit(self.board_img, self.BOARD_POS,
                         self.board_img.get_rect())
        self.put_piece((3, 3), WHITE)
        self.put_piece((4, 4), WHITE)
        self.put_piece((3, 4), BLACK)
        self.put_piece((4, 3), BLACK)
        # defualt method
        pygame.display.flip()

    # put checkers using given pos
    def put_piece(self, pos, color):
        if pos == None:
            # todo raise excptions
            return

        # flip orientation (because xy screen orientation)
        pos = (pos[1], pos[0])

        if color == BLACK:
            img = self.black_img
        elif color == WHITE:
            img = self.white_img
        else:
            img = self.tip_img

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]

        self.screen.blit(img, (x, y), img.get_rect())
        pygame.display.flip()

    # clean every unusual
    def clear_square(self, pos):
        pos = (pos[1], pos[0])

        x = pos[0] * self.SQUARE_SIZE + self.BOARD[0]
        y = pos[1] * self.SQUARE_SIZE + self.BOARD[1]
        self.screen.blit(self.clear_img, (x, y), self.clear_img.get_rect())
        pygame.display.flip()

    def clear_all(self, valids):
        for pos in valids:
            self.clear_square(pos)

    def get_mouse_input(self):
        while True:
            for event in pygame.event.get():
                # returns tuple
                if event.type == MOUSEBUTTONDOWN:
                    (mouse_x, mouse_y) = pygame.mouse.get_pos()

                    # handle wrong click (out of board)
                    if mouse_x > self.BOARD_SIZE + self.BOARD[0] or \
                            mouse_x < self.BOARD[0] or \
                            mouse_y > self.BOARD_SIZE + self.BOARD[1] or \
                            mouse_y < self.BOARD[1]:
                        continue

                    # find that place
                    position = ((mouse_x - self.BOARD[0]) // self.SQUARE_SIZE), \
                               ((mouse_y - self.BOARD[1]) // self.SQUARE_SIZE)
                    # flip orientation
                    position = (position[1], position[0])
                    return position

                elif event.type == QUIT:
                    sys.exit(0)

            time.sleep(.05)

    # end of each iteration
    def update(self, board, blacks, whites, current_player_color):
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    self.put_piece((i, j), board[i][j])

        blacks_str = '%02d ' % int(blacks)
        whites_str = '%02d ' % int(whites)
        self.show_score(blacks_str, whites_str, current_player_color)
        pygame.display.flip()

    def show_score(self, blackStr, whiteStr, current_player_color):
        black_background = self.YELLOW if current_player_color == WHITE else self.BACKGROUND
        white_background = self.YELLOW if current_player_color == BLACK else self.BACKGROUND
        text = self.scoreFont.render(blackStr, True, self.BLACK,
                                     black_background)
        text2 = self.scoreFont.render(whiteStr, True, self.WHITE,
                                      white_background)
        self.screen.blit(text,
                         (self.BLACK_LAB_POS[0], self.BLACK_LAB_POS[1] + 40))
        self.screen.blit(text2,
                         (self.WHITE_LAB_POS[0], self.WHITE_LAB_POS[1] + 40))

    def wait_quit(self):
        # wait user to close window
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                break

    # to handle next phase
    def show_valid_moves(self, valid_moves,bestie):
        logger.debug('valid movies: %s', valid_moves)
        logger.debug('best valid movies: %s', bestie)
        for move in valid_moves:
            self.put_piece(move, 'tip')
