from config import *


class Evaluator(object):

    def __init__(self, vec=None):
        if vec is None:
            vec = BESTGENE
        self.WIPEOUT_SCORE = vec[0]  # a move that results a player losing all pieces
        self.PIECE_COUNT_WEIGHT = vec[1]
        self.POTENTIAL_MOBILITY_WEIGHT = vec[2]
        self.MOBILITY_WEIGHT = vec[3]
        self.CORNER_WEIGHT = vec[4]
        self.EDGE_WEIGHT = vec[5]
        self.XSQUARE_WEIGHT = vec[6]

    def get_piece_differential(self, diffBoard, game_band):

        if self.PIECE_COUNT_WEIGHT[game_band] != 0:
            whites, blacks, empty = diffBoard.get_changes()
            if self.player == WHITE:
                myScore = whites
                op_score = blacks
            else:
                myScore = blacks
                op_score = whites
            return self.PIECE_COUNT_WEIGHT[game_band] * (myScore - op_score)
        return 0

    def get_corner_differential(self, diffCount, diffBoard, game_band):
        if self.CORNER_WEIGHT[game_band] != 0:
            # corner differential
            myScore = 0
            op_score = 0
            for i in [0, 7]:
                for j in [0, 7]:
                    if diffBoard.board[i][j] == self.player:
                        myScore += 1
                    elif diffBoard.board[i][j] == self.enemy:
                        op_score += 1
                    if myScore + op_score >= diffCount:
                        break
                if myScore + op_score >= diffCount:
                    break
            return self.CORNER_WEIGHT[game_band] * (myScore - op_score)
        return 0

    def get_edge_differential(self, diffCount, diffBoard, game_band):
        if self.EDGE_WEIGHT[game_band] != 0:
            myScore = 0
            op_score = 0
            squares = [(a, b) for a in [0, 7] for b in range(1, 7)] \
                      + [(a, b) for a in range(1, 7) for b in [0, 7]]

            for x, y in squares:
                if diffBoard.board[x][y] == self.player:
                    myScore += 1
                elif diffBoard.board[x][y] == self.enemy:
                    op_score += 1
                if myScore + op_score >= diffCount:
                    break
            return self.EDGE_WEIGHT[game_band] * (myScore - op_score)

        return 0

    def get_xsquare_differential(self, startBoard, currentBoard, deltaBoard, game_band):
        if self.XSQUARE_WEIGHT[game_band] != 0:
            myScore = 0
            yourScore = 0
            for x, y in [(a, b) for a in [1, 6] for b in [1, 6]]:
                if deltaBoard.board[x][y] != EMPTY and startBoard.board[x][y] == EMPTY:
                    # if the piece is new consider this square if the nearest
                    # corner is open
                    cornerx = x
                    cornery = y
                    if cornerx == 1:
                        cornerx = 0
                    elif cornerx == 6:
                        cornerx = 7
                    if cornery == 1:
                        cornery = 0
                    elif cornery == 6:
                        cornery = 7
                    if currentBoard.board[cornerx][cornery] == EMPTY:
                        if currentBoard.board[x][y] == self.player:
                            myScore += 1
                        elif currentBoard.board[x][y] == self.enemy:
                            yourScore += 1
            return self.XSQUARE_WEIGHT[game_band] * (myScore - yourScore)
        return 0

    # doresho mishmare ba komak in method bebine hanuz cheghade mitune bere -> boro tuye board in method o bebin motevajeh mshi
    # todo badesh in commento pak konim ghable upload :))
    def get_potential_mobility_differential(self, startBoard, currentBoard, game_band):
        if self.POTENTIAL_MOBILITY_WEIGHT[game_band] != 0:
            myScore = currentBoard.get_adjacent_count(
                self.enemy) - startBoard.get_adjacent_count(self.enemy)
            yourScore = currentBoard.get_adjacent_count(
                self.player) - startBoard.get_adjacent_count(self.player)
            return self.POTENTIAL_MOBILITY_WEIGHT[game_band] * (myScore - yourScore)
        return 0

    # in tedade harekatayi k harki dare ro kam mkne az ham emtiaz mide
    def get_mobility_differential(self, startBoard, currentBoard, game_band):
        myScore = len(currentBoard.get_best_valid_moves(self.player)) - \
                  len(startBoard.get_best_valid_moves(self.player))
        yourScore = len(currentBoard.get_best_valid_moves(
            self.enemy)) - len(startBoard.get_best_valid_moves(self.enemy))
        return self.MOBILITY_WEIGHT[game_band] * (myScore - yourScore)

    def evaluate_all_heuristics(self, startBoard, board, currentDepth, player, opponent):
        self.player = player
        self.enemy = opponent
        sc = 0
        game_band = 0
        whites, blacks, empty = board.get_changes()

        piece_count = whites+blacks



        deltaBoard = board.compare(startBoard)
        deltaCount = sum(deltaBoard.get_changes())


        # check kardane un harekate k bazio tamum mikard.
        if (self.player == WHITE and whites == 0) or (self.player == BLACK and blacks == 0):
            return -self.WIPEOUT_SCORE
        if (self.enemy == WHITE and whites == 0) or (self.enemy == BLACK and blacks == 0):
            return self.WIPEOUT_SCORE

        # game situation
        if piece_count <= 16:
            game_band = 0
        elif piece_count <= 32:
            game_band = 1
        elif piece_count <= 48:
            game_band = 2
        elif piece_count <= 64 - currentDepth:
            game_band = 3
        else:
            game_band = 4

        sc += self.get_corner_differential(deltaCount, deltaBoard, game_band)
        sc += self.get_edge_differential(deltaCount, deltaBoard, game_band)
        sc += self.get_xsquare_differential(startBoard,
                                            board, deltaBoard, game_band)

        sc += self.get_potential_mobility_differential(startBoard, board, game_band)
        sc += self.get_mobility_differential(startBoard, board, game_band)

        sc += self.get_piece_differential(deltaBoard, game_band)
        return sc
