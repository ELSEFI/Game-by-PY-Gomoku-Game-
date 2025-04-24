#Edited by kareem hany 

import pygame
from gomoku_board import CELL_SIZE, GRID_SIZE, OFFSET_X, OFFSET_Y, WHITE, GRAY, BLACK, LIGHT_GRAY, RED

class GameUI:
    def __init__(self, screen, board):
        # Initialize UI with screen, board, and fonts
        self.screen = screen
        self.board = board
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 30)

    def draw_board(self):
        # Fill screen with white color as background
        self.screen.fill(WHITE)

        # Draw grid lines
        for i in range(GRID_SIZE):
            pygame.draw.line(
                self.screen, GRAY,
                (OFFSET_X + CELL_SIZE // 2, OFFSET_Y + CELL_SIZE // 2 + i * CELL_SIZE),
                (OFFSET_X + CELL_SIZE // 2 + (GRID_SIZE - 1) * CELL_SIZE, OFFSET_Y + CELL_SIZE // 2 + i * CELL_SIZE),
                2
            )
            pygame.draw.line(
                self.screen, GRAY,
                (OFFSET_X + CELL_SIZE // 2 + i * CELL_SIZE, OFFSET_Y + CELL_SIZE // 2),
                (OFFSET_X + CELL_SIZE // 2 + i * CELL_SIZE, OFFSET_Y + CELL_SIZE // 2 + (GRID_SIZE - 1) * CELL_SIZE),
                2
            )

        # Draw row and column labels (numbers)
        for i in range(GRID_SIZE):
            label = self.small_font.render(str(i + 1), True, BLACK)
            label_rect_h = label.get_rect(center=(OFFSET_X + CELL_SIZE // 2 + i * CELL_SIZE, OFFSET_Y - 30))
            self.screen.blit(label, label_rect_h)

            label_rect_v = label.get_rect(center=(OFFSET_X - 30, OFFSET_Y + CELL_SIZE // 2 + i * CELL_SIZE))
            self.screen.blit(label, label_rect_v)

        # Draw the game pieces (black or white)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                piece = self.board.grid[y][x]
                if piece == 1:
                    # Draw black piece
                    pygame.draw.circle(self.screen, BLACK,
                        (OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2,
                         OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2 - 4)
                    # Highlight last move with a red circle around the piece
                    if self.board.last_move == (x, y):
                        pygame.draw.circle(self.screen, RED,
                            (OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2,
                             OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 2 - 4, 2)
                elif piece == 2:
                    # Draw white piece
                    pygame.draw.circle(self.screen, LIGHT_GRAY,
                        (OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2,
                         OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2 - 4)
                    # Highlight last move with a red circle around the piece
                    if self.board.last_move == (x, y):
                        pygame.draw.circle(self.screen, RED,
                            (OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2,
                             OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2),
                            CELL_SIZE // 2 - 4, 2)

    def draw_text(self, text, pos, color=BLACK, small=False):
        # Draw text on the screen at the specified position
        font = self.small_font if small else self.font
        render = font.render(text, True, color)
        self.screen.blit(render, pos)

    def update_display(self):
        # Update the screen display
        pygame.display.flip()
