import pygame
import random
import player
import board
from config import BLACK, WHITE, HUMAN
import log

logger = log.setup_custom_logger('root')

class learningOthello:

    def __init__(self,player1vec=None,player2vec=None):
        # start
        self.board = board.Board()
        self.start(player1vec,player2vec)

    def start(self,player1vec,player2vec):
        logger.info('startGame: \n   player 1: %s --- player 2: %s ', player1vec, player2vec)
        self.now_playing = player.Computer(BLACK,vec=player1vec)
        self.other_player = player.Computer(WHITE,vec=player2vec)


    def run(self):

        while True:
            if self.board.game_ended():
                whites, blacks, empty = self.board.get_changes()
                return whites,blacks

            self.now_playing.get_current_board(self.board)
            valid_moves = self.board.get_valid_moves(self.now_playing.color)
            if valid_moves != []:
                score, self.board = self.now_playing.get_move()

            self.now_playing, self.other_player = self.other_player, self.now_playing

            #print("change",self.board.get_changes())
