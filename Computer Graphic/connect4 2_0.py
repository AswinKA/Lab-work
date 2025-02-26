import pygame
import sys
import time
pygame.font.init()  # Initialize the font module

# Define constants
no_row = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
MYFONT = pygame.font.SysFont("monospace", 33)
CYAN = (0, 255, 255)
GRAY = (169, 169, 169)
LIGHT_BLUE = (173, 216, 230)  # New color for win messages

# Initialize pygame
pygame.init()

# Set up the game window
width = COLUMN_COUNT * SQUARESIZE
height = (no_row + 1) * SQUARESIZE
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")

# Create the game board
def create_board():
    board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(no_row)]
    return board

# Draw the game board
def draw_board(board, winner_coords=None, timer=None, message=None, prompt=None, turn=0, posx=None):
    screen.fill(BLACK)  # Clear the screen once at the beginning of each loop
    
    # Draw the game board and the circles for the tokens
    for c in range(COLUMN_COUNT):
        for r in range(no_row):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    # Draw the tokens and their colors
    for c in range(COLUMN_COUNT):
        for r in range(no_row):
            piece = board[r][c]
            
            # Determine the color of the piece
            if winner_coords and (r, c) in winner_coords:
                color = CYAN  # Winning piece turns cyan
            elif piece == 1:
                color = RED  # Red for PLAYER1
            elif piece == 2:
                color = YELLOW  # Yellow for PLAYER2
            else:
                continue  # Skip empty spaces
            
            # Turn non-winning pieces grey
            if winner_coords and (r, c) not in winner_coords and piece != 0:
                color = GRAY
            
            pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    # Show the message in the center of the screen if provided
    if message:
        message_text = MYFONT.render(message, 1, LIGHT_BLUE)  # Use LIGHT_BLUE for the win message
        screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height // 2 - message_text.get_height() // 2))

    # Show the play again prompt below the win message if provided
    if prompt:
        prompt_text = MYFONT.render(prompt, 1, LIGHT_BLUE)
        screen.blit(prompt_text, (width // 2 - prompt_text.get_width() // 2, height // 2 + message_text.get_height() // 2 + 10))

    # Show the timer for the current player
    if timer is not None:
        timer_text = MYFONT.render(f"{timer}s", 1, CYAN)
        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))  # Black rectangle for the timer area
        screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 10))

    # Show the preview token over the column (if moving token)
    if posx is not None:
        pygame.draw.circle(screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)

# Check if a column is valid for a move
def is_valid_location(board, col):
    return board[no_row - 1][col] == 0

# Get the next available row in a column
def get_next_available_row(board, col):
    for r in range(no_row):
        if board[r][col] == 0:
            return r

# Drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check for a win condition
def winning_move(board, piece):
    winning_coords = []

    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(no_row):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                winning_coords = [(r, c), (r, c + 1), (r, c + 2), (r, c + 3)]
                return winning_coords

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(no_row - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                winning_coords = [(r, c), (r + 1, c), (r + 2, c), (r + 3, c)]
                return winning_coords

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(no_row - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                winning_coords = [(r, c), (r + 1, c + 1), (r + 2, c + 2), (r + 3, c + 3)]
                return winning_coords

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, no_row):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                winning_coords = [(r, c), (r - 1, c + 1), (r - 2, c + 2), (r - 3, c + 3)]
                return winning_coords

    return None

# Main game loop
def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 for Red, 1 for Yellow
    last_time = time.time()
    timer = 10  # 10 seconds for each player
    message = None
    prompt = None
    posx = None  # Store the x position of the preview token

    while not game_over:
        winner_coords = None  # Default to no winner
        message = None  # Reset message for each loop
        prompt = None  # Reset prompt for each loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEMOTION:
                # Move the token across the board, update position (without flickering)
                posx = event.pos[0]
                
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_available_row(board, col)
                    drop_piece(board, row, col, 1 if turn == 0 else 2)

                    winner_coords = winning_move(board, 1 if turn == 0 else 2)
                    if winner_coords:
                        message = f"PLAYER {('RED' if turn == 0 else 'YELLOW')} WINS!"
                        prompt = "Press Enter to Play Again"
                        game_over = True

                    turn += 1
                    turn = turn % 2  # Switch player

                    last_time = time.time()  # Reset the timer when the player makes a move
                    draw_board(board, winner_coords, timer, message, prompt, turn, posx)
                    pygame.display.update()

        # Track time for the current player
        elapsed_time = int(time.time() - last_time)
        remaining_time = max(0, 10 - elapsed_time)  # 10 seconds limit

        if remaining_time == 0:
            message = f"PLAYER {('RED' if turn == 0 else 'YELLOW')} LOSES!"
            prompt = None  # No prompt for play again if the player loses
            game_over = True
            pygame.display.update()

        draw_board(board, winner_coords, remaining_time, message, prompt, turn, posx)

        pygame.display.update()

    # Wait 10 seconds before asking to play again
    pygame.time.wait(10000)

    # Ask if the player wants to play again
    play_again_prompt = MYFONT.render("Press Enter to Play Again", 1, LIGHT_BLUE)
    screen.blit(play_again_prompt, (width // 2 - play_again_prompt.get_width() // 2, height // 2 + 60))

    play_again_exit = MYFONT.render("or any key to Exit", 1, LIGHT_BLUE)
    screen.blit(play_again_exit, (width // 2 - play_again_exit.get_width() // 2, height // 2 + 120))

    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()  # Restart the game
                else:
                    pygame.quit()
                    sys.exit()

# Start the game
if __name__ == "__main__":
    draw_board(create_board(), None, 10, None, 0, None)
    main()
    pygame.quit()
    sys.exit()
