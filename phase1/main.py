import pygame
from othelo import *



FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Othello')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    program_run = True

    while program_run:
        game_run = True
        Clock = pygame.time.Clock()
        board = Board()

        while game_run:
            Clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_run = False
                    game_run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    #
                    board.insert(row, col, WINDOW)

            if board.draw(WINDOW) == "end":
                game_run = False

            pygame.display.update()

        while program_run and not game_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if board.check_position_in_end_page(pos) == "quit":
                        program_run = False
                    elif board.check_position_in_end_page(pos) == "restart":
                        game_run = True

            board.draw_end_game(WINDOW)
            pygame.display.update()

    pygame.quit()


main()
