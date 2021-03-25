import pygame
import ui
import player
import board
from config import BLACK, WHITE, HUMAN
import log

logger = log.setup_custom_logger('root')
'''
main class of othello
'''


class Othello:

    def __init__(self):

        # start
        self.gui = ui.Gui()
        self.board = board.Board()
        self.gui.show_menu(self.start)

    def start(self, *args):
        player1, player2 = args
        logger.info('Settings: player 1: %s, player 2: %s ', player1, player2)
        if player1 == HUMAN:
            self.now_playing = player.Human(self.gui, BLACK)
        else:
            self.now_playing = player.Computer(BLACK)
        if player2 == HUMAN:
            self.other_player = player.Human(self.gui, WHITE)
        else:
            self.other_player = player.Computer(WHITE)

        self.gui.show_game()
        self.gui.update(self.board.board, 2, 2, self.now_playing.color)
        print("end of start")


    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            if self.board.game_ended():
                whites, blacks, empty = self.board.get_changes()
                if whites > blacks:
                    winner = WHITE
                elif blacks > whites:
                    winner = BLACK
                else:
                    winner = None
                break
            self.now_playing.get_current_board(self.board)
            valid_moves = self.board.get_valid_moves(self.now_playing.color)
            bestie = self.board.get_best_valid_moves(self.now_playing.color)
            if valid_moves != []:
                self.gui.show_valid_moves(valid_moves,bestie)
                score, self.board = self.now_playing.get_move()
                whites, blacks, empty = self.board.get_changes()
                self.gui.clear_all(valid_moves)
                self.gui.update(self.board.board, blacks, whites,
                                self.now_playing.color)

            self.now_playing, self.other_player = self.other_player, self.now_playing
        self.gui.show_winner(winner)
        pygame.time.wait(500)
        self.restart()

    def restart(self):
        self.board = board.Board()
        self.gui.show_menu(self.start)
        self.run()


def main():
    game = Othello()
    game.run()


if __name__ == '__main__':
    main()
