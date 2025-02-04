import pygame
import sys
import numpy as np

# Constants
BOARD_SIZE = 8
TILE_SIZE = 80
SCREEN_SIZE = BOARD_SIZE * TILE_SIZE
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# Colors for players
PLAYER1_COLOR = BLACK
PLAYER2_COLOR = WHITE

# Directions for flipping tiles
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

class ReversiGame:
    def __init__(self):
        # Initialize game board: 0 for empty, 1 for black, 2 for white
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = 1
        
        # Initial setup
        self.board[3][3], self.board[4][4] = 2, 2  # White tiles
        self.board[3][4], self.board[4][3] = 1, 1  # Black tiles

    def draw_board(self, screen):
        screen.fill(GREEN)
        
        # Draw grid
        for x in range(0, SCREEN_SIZE, TILE_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_SIZE))
            pygame.draw.line(screen, BLACK, (0, x), (SCREEN_SIZE, x))
        
        # Draw tiles
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != 0:
                    color = PLAYER1_COLOR if self.board[row][col] == 1 else PLAYER2_COLOR
                    pygame.draw.circle(screen, color, 
                                       (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2),
                                       TILE_SIZE // 2 - 5)

    def is_valid_move(self, row, col, player):
        if self.board[row][col] != 0:
            return False

        opponent = 2 if player == 1 else 1
        valid = False

        for dx, dy in DIRECTIONS:
            x, y = row + dx, col + dy
            tiles_to_flip = []

            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == opponent:
                tiles_to_flip.append((x, y))
                x += dx
                y += dy

            if tiles_to_flip and 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == player:
                valid = True

        return valid

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def place_tile(self, row, col):
        if not self.is_valid_move(row, col, self.current_player):
            return False

        opponent = 2 if self.current_player == 1 else 1
        tiles_to_flip = []

        for dx, dy in DIRECTIONS:
            x, y = row + dx, col + dy
            potential_flips = []

            while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == opponent:
                potential_flips.append((x, y))
                x += dx
                y += dy

            if potential_flips and 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == self.current_player:
                tiles_to_flip.extend(potential_flips)

        # Place the tile and flip captured tiles
        self.board[row][col] = self.current_player
        for x, y in tiles_to_flip:
            self.board[x][y] = self.current_player

        # Switch players
        self.current_player = 2 if self.current_player == 1 else 1
        return True

    def get_winner(self):
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == 2)
        if black_count > white_count:
            return "Black wins!"
        elif white_count > black_count:
            return "White wins!"
        else:
            return "It's a tie!"

    def has_valid_moves(self, player):
        return len(self.get_valid_moves(player)) > 0

    def display_winner_message(self, screen):
        font = pygame.font.Font(None, 74)
        winner_message = self.get_winner()
        text_surface = font.render(winner_message, True, CYAN)
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def display_player_turn(self, screen):
        font = pygame.font.Font(None, 36)
        player_message = f"Player {'Black' if self.current_player == 1 else 'White'}'s Turn"
        text_surface = font.render(player_message, True, RED)
        screen.blit(text_surface, (10, SCREEN_SIZE - 40))

    def highlight_valid_moves(self, screen):
        valid_moves = self.get_valid_moves(self.current_player)
        for row, col in valid_moves:
            pygame.draw.circle(screen, BLUE, 
                               (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2),
                               5)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + 40))  # Extra space for turn display
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()
    game = ReversiGame()

    running = True
    game_over = False

    while running:
        screen.fill(GREEN)
        game.draw_board(screen)
        game.highlight_valid_moves(screen)
        game.display_player_turn(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                if y < SCREEN_SIZE:
                    row, col = y // TILE_SIZE, x // TILE_SIZE

                    if game.place_tile(row, col):
                        # Update display immediately after a valid move
                        screen.fill(GREEN)
                        game.draw_board(screen)
                        game.display_player_turn(screen)
                        pygame.display.flip()

                        if not (game.has_valid_moves(1) or game.has_valid_moves(2)):
                            game_over = True
                            game.display_winner_message(screen)
                            break  # Ensure winner message shows after last move

        # Check if neither player has valid moves and declare the winner based on chip count
        if not (game.has_valid_moves(1) or game.has_valid_moves(2)) and not game_over:
            game_over = True
            game.display_winner_message(screen)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
 