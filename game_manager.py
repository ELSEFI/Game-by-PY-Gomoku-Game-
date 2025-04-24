import pygame
import asyncio
import sys
from gomoku_board import GomokuBoard
from game_ui import GameUI
from gomoku_board import WINDOW_WIDTH, WINDOW_HEIGHT, OFFSET_X, OFFSET_Y, CELL_SIZE, FPS, BLUE, RED, YELLOW
from gomoku_board import WHITE, BLACK, GRAY, LIGHT_GRAY
from gomoku_board import GomokuBoard, GRID_SIZE, AIPlayer

class GameManager:
    def __init__(self):
        # Initialize pygame and set up the game window
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gomoku 15x15")
        self.clock = pygame.time.Clock()
        
        # Initialize the game board and UI
        self.board = GomokuBoard(GRID_SIZE)
        self.ui = GameUI(self.screen, self.board)
        
        # Set up the initial game state
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.ai_thinking = False
        self.game_mode = None  # None: selection screen, "ai": vs AI, "human": vs human
        self.ai = None  # Will be initialized when AI mode is selected
        self.setup_buttons()

    def get_dynamic_depth(self):
        # Calculate AI search depth based on the number of moves made so far
        total_moves = sum(cell != 0 for row in self.board.grid for cell in row)
        if total_moves < 10:
            return 2
        elif total_moves < 20:
            return 3
        elif total_moves < 30:
            return 4
        else:
            return 3  # Reduce depth in later stages to avoid slowness

    def setup_buttons(self):
        # Define button dimensions and position for mode selection and game controls
        button_width = 200
        button_height = 50
        center_x = WINDOW_WIDTH // 2
        
        # Mode selection buttons: AI vs Human or Human vs Human
        self.ai_button = pygame.Rect(center_x - button_width - 20, WINDOW_HEIGHT // 2 - button_height // 2, button_width, button_height)
        self.human_button = pygame.Rect(center_x + 20, WINDOW_HEIGHT // 2 - button_height // 2, button_width, button_height)
        
        # Play again and close buttons for after game ends
        self.play_again_button = pygame.Rect(center_x - button_width - 20, WINDOW_HEIGHT - 80, button_width, button_height)
        self.close_button = pygame.Rect(center_x + 20, WINDOW_HEIGHT - 80, button_width, button_height)

    async def ai_turn(self):
        # Handle the AI's turn, including thinking animation and move calculation
        self.ai_thinking = True
        self.ui.draw_text("AI Thinking...", (WINDOW_WIDTH // 2 - 100, 20), RED, small=True)
        self.ui.update_display()
        
        # Initialize AI if not already done
        if self.ai is None:
            self.ai = AIPlayer(self.board)
        
        # Set AI's search depth based on game progress
        self.ai.depth = self.get_dynamic_depth()
        
        try:
            # Wait for AI to decide on a move with a 2-second timeout
            move = await asyncio.wait_for(self.ai.get_best_move(), timeout=2.0)
        except asyncio.TimeoutError:
            # If AI doesn't decide in time, pick an empty nearby cell
            empty_cells = self.board.get_nearby_cells()
            move = empty_cells[0] if empty_cells else None
        
        self.ai_thinking = False
        
        # If a valid move is found, apply it and check for a win
        if move:
            x, y = move
            self.board.make_move(x, y, 2)
            if self.board.check_win(x, y, 2):
                self.winner = 2
                self.game_over = True

    def handle_click(self, pos):
        # Handle click events for mode selection and game actions
        if self.game_mode is None:
            # Mode selection screen
            if self.ai_button.collidepoint(pos):
                self.game_mode = "ai"
                self.ai = AIPlayer(self.board)  # Initialize AI for AI mode
                return
            elif self.human_button.collidepoint(pos):
                self.game_mode = "human"
                return
            return

        # Game over screen buttons
        if self.game_over:
            if self.play_again_button.collidepoint(pos):
                self.reset_game()
                return
            elif self.close_button.collidepoint(pos):
                pygame.quit()
                sys.exit()
                return
        
        # Regular game play
        if self.ai_thinking or self.game_over:
            return
            
        # Determine which cell was clicked and make the move if valid
        mx, my = pos
        mx -= OFFSET_X
        my -= OFFSET_Y
        x = mx // CELL_SIZE
        y = my // CELL_SIZE
        if self.board.is_valid_move(x, y):
            self.board.make_move(x, y, self.current_player)
            if self.board.check_win(x, y, self.current_player):
                self.winner = self.current_player
                self.game_over = True
            else:
                # Switch player after valid move
                self.current_player = 2 if self.current_player == 1 else 1

    def reset_game(self):
        # Reset the game state for a new game
        self.board.reset()
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.ai_thinking = False

    def draw_mode_selection(self):
        # Draw the mode selection screen with buttons for "Play vs AI" and "Play vs Human"
        self.screen.fill(WHITE)
        self.ui.draw_text("Choose Game Mode", (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 4), BLUE)
        
        # Draw AI mode button
        pygame.draw.rect(self.screen, GRAY, self.ai_button)
        self.ui.draw_text("Play vs AI", (self.ai_button.x + 35, self.ai_button.y + 10), BLACK, small=True)
        
        # Draw Human mode button
        pygame.draw.rect(self.screen, GRAY, self.human_button)
        self.ui.draw_text("Play vs Human", (self.human_button.x + 20, self.human_button.y + 10), BLACK, small=True)

    def draw_game_over_buttons(self):
        # Draw the game over buttons (Play Again and Close Game)
        pygame.draw.rect(self.screen, GRAY, self.play_again_button)
        self.ui.draw_text("Play Again", (self.play_again_button.x + 35, self.play_again_button.y + 10), BLACK, small=True)
        
        pygame.draw.rect(self.screen, GRAY, self.close_button)
        self.ui.draw_text("Close Game", (self.close_button.x + 30, self.close_button.y + 10), BLACK, small=True)

    async def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            if self.game_mode is None:
                self.draw_mode_selection()
            else:
                # Draw the board and handle game-over or AI thinking states
                self.ui.draw_board()
                
                if self.ai_thinking:
                    self.ui.draw_text("AI Thinking...", (WINDOW_WIDTH // 2 - 100, 20), RED, small=True)
                elif self.game_over:
                    if self.winner:
                        self.ui.draw_text(f"Player {self.winner} Wins!", (WINDOW_WIDTH // 2 - 120, 20), RED)
                    else:
                        self.ui.draw_text("Draw!", (WINDOW_WIDTH // 2 - 60, 20), RED)
                    # Draw the game over buttons
                    self.draw_game_over_buttons()
                else:
                    self.ui.draw_text(f"Player {self.current_player}'s Turn", (WINDOW_WIDTH - 250, 20), BLUE, small=True)

            self.ui.update_display()

            # AI turn if it's AI's move and the game is not over
            if not self.game_over and self.game_mode == "ai" and self.current_player == 2 and not self.ai_thinking:
                await self.ai_turn()
                self.current_player = 1

            await asyncio.sleep(0.01)  # Reduce delay to improve UI responsiveness
