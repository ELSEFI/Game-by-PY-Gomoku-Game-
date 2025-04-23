# Edited by Mohamed Elsefi & Zeyad Ibrahim
import pygame
import sys
import asyncio
import platform
import copy

# Constants for cell size, grid size, and window dimensions
CELL_SIZE = 60
GRID_SIZE = 15
BOARD_SIZE = CELL_SIZE * GRID_SIZE
OFFSET_X = 60
OFFSET_Y = 100
WINDOW_WIDTH = BOARD_SIZE + OFFSET_X
WINDOW_HEIGHT = BOARD_SIZE + OFFSET_Y

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
LIGHT_GRAY = (220, 220, 220)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Frames per second for the game
FPS = 60
MAX_DEPTH = 2  # Maximum depth for Minimax algorithm

class GomokuBoard:
    def __init__(self, size):
        """Initialize the Gomoku board with a given size."""
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # Create an empty board
        self.last_move = None  # Track the last move made

    def reset(self):
        """Reset the board to its initial state."""
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = None

    def is_valid_move(self, x, y):
        """Check if a move is valid by ensuring the coordinates are within bounds and the cell is empty."""
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x] == 0

    def make_move(self, x, y, player):
        """Make a move for a player (1 or 2) on the board at the specified coordinates."""
        if self.is_valid_move(x, y):
            self.grid[y][x] = player
            self.last_move = (x, y)
            return True
        return False

    def check_win(self, x, y, player):
        """Check if the specified player has won the game by forming a line of 5 consecutive pieces."""
        def count(dx, dy):
            """Count consecutive pieces in a given direction."""
            cnt = 0
            nx, ny = x + dx, y + dy
            while 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == player:
                cnt += 1
                nx += dx
                ny += dy
            return cnt

        # Define directions to check: horizontal, vertical, and diagonal lines
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if count(dx, dy) + count(-dx, -dy) + 1 >= 5:
                return True
        return False

    def get_nearby_cells(self):
        """Get a list of cells that are near the last move or empty cells if no move has been made."""
        cells = set()
        if self.last_move:
            x, y = self.last_move
            for dy in [-2, -1, 0, 1, 2]:
                for dx in [-2, -1, 0, 1, 2]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == 0:
                        cells.add((nx, ny))
        else:
            for y in range(self.size):
                for x in range(self.size):
                    if self.grid[y][x] != 0:
                        for dy in [-2, -1, 0, 1, 2]:
                            for dx in [-2, -1, 0, 1, 2]:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == 0:
                                    cells.add((nx, ny))
        return list(cells) if cells else [(self.size // 2, self.size // 2)]  # Return the center if no nearby cells

class AIPlayer:
    def __init__(self, board, depth=MAX_DEPTH):
        """Initialize the AI player with a reference to the board and search depth for Minimax."""
        self.board = board
        self.depth = depth

    def order_moves(self, moves):
        """Order possible moves by priority, considering central position, distance from last move, and threat evaluation."""
        ordered = []
        for x, y in moves:
            priority = 0
            if 5 <= x <= 9 and 5 <= y <= 9:  # Give priority to central moves
                priority += 10
            if self.board.last_move:
                lx, ly = self.board.last_move
                distance = abs(x - lx) + abs(y - ly)  # Priority based on distance from last move
                priority += (10 - distance)
            self.board.grid[y][x] = 2  # Evaluate the move by making it temporarily
            score = self.evaluate()  # Get the evaluation score
            self.board.grid[y][x] = 0  # Revert the move
            priority += score // 100  # Add score-based weight
            ordered.append((priority, (x, y)))
        ordered.sort(reverse=True)  # Sort moves by priority
        return [move for _, move in ordered]

    def evaluate(self):
        """Evaluate the current board state and return a score based on possible threats and opportunities."""
        score = 0
        for y in range(self.board.size):
            for x in range(self.board.size):
                player = self.board.grid[y][x]
                if player == 0:
                    continue
                multiplier = 1 if player == 2 else -1
                for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                    count = 0
                    open_ends = 0
                    for i in range(-4, 5):  # Check for lines of 5 pieces in different directions
                        nx, ny = x + i * dx, y + i * dy
                        if 0 <= nx < self.board.size and 0 <= ny < self.board.size:
                            if self.board.grid[ny][nx] == player:
                                count += 1
                            else:
                                if self.board.grid[ny][nx] == 0:
                                    open_ends += 1
                                count = 0
                        else:
                            count = 0
                        if count == 2:
                            score += (50 if open_ends >= 1 else 10) * multiplier
                        elif count == 3:
                            score += (500 if open_ends >= 1 else 100) * multiplier
                        elif count == 4:
                            score += (5000 if open_ends >= 1 else 1000) * multiplier
                        elif count >= 5:
                            score += 100000 * multiplier
                    if 5 <= x <= 9 and 5 <= y <= 9 and self.board.grid[y][x] == player:
                        score += 5 * multiplier  # Add score for central positions
        return score

    def minimax(self, depth, alpha, beta, maximizing):
        """Minimax algorithm to evaluate the best possible move by recursively exploring the game tree."""
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] != 0 and self.board.check_win(x, y, self.board.grid[y][x]):
                    return 100000 if self.board.grid[y][x] == 2 else -100000

        if depth == 0:  # Base case: evaluate at maximum depth
            return self.evaluate()

        empty_cells = self.order_moves(self.board.get_nearby_cells())
        if maximizing:  # Maximize the score for AI's turn
            max_eval = -float('inf')
            for x, y in empty_cells:
                self.board.grid[y][x] = 2
                eval_score = self.minimax(depth - 1, alpha, beta, False)
                self.board.grid[y][x] = 0
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:  # Beta pruning
                    break
            return max_eval
        else:  # Minimize the score for the opponent's turn
            min_eval = float('inf')
            for x, y in empty_cells:
                self.board.grid[y][x] = 1
                eval_score = self.minimax(depth - 1, alpha, beta, True)
                self.board.grid[y][x] = 0
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:  # Beta pruning
                    break
            return min_eval

    async def get_best_move(self):
        """Get the best move for the AI by analyzing the board using Minimax."""
        total_moves = sum(self.board.grid[y][x] != 0 for y in range(self.board.size) for x in range(self.board.size))
        if total_moves < 2:  # Handle first two moves separately (center strategy)
            center = self.board.size // 2
            if self.board.grid[center][center] == 0:
                return (center, center)
            elif self.board.grid[center][center - 1] == 0:
                return (center, center - 1)

        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        # Check for immediate winning move or blocking move
        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    self.board.grid[y][x] = 2
                    if self.board.check_win(x, y, 2):  # Check if AI can win
                        self.board.grid[y][x] = 0
                        return (x, y)
                    self.board.grid[y][x] = 0

        for y in range(self.board.size):
            for x in range(self.board.size):
                if self.board.grid[y][x] == 0:
                    self.board.grid[y][x] = 1
                    if self.board.check_win(x, y, 1):  # Check if opponent can win
                        self.board.grid[y][x] = 0
                        return (x, y)
                    self.board.grid[y][x] = 0

        empty_cells = self.order_moves(self.board.get_nearby_cells())
        for x, y in empty_cells:
            self.board.grid[y][x] = 2
            score = self.minimax(self.depth - 1, alpha, beta, False)
            self.board.grid[y][x] = 0
            if score > best_score:
                best_score = score
                best_move = (x, y)
            alpha = max(alpha, score)  # Alpha pruning
        return best_move
