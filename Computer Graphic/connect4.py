import pygame
import sys
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
MYFONT = pygame.font.SysFont("monospace", 65)
CYAN =(0, 255, 255)

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
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(no_row):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(no_row):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

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
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(no_row):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(no_row - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(no_row - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, no_row):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

    return False

# Main game loop
def main():
    board = create_board()
    game_over = False
    turn = 0  # 0 for Red, 1 for Yellow

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, RED if turn == 0 else YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_available_row(board, col)
                    drop_piece(board, row, col, 1 if turn == 0 else 2)

                    if winning_move(board, 1 if turn == 0 else 2):
                        label = MYFONT.render(f"Player {('Red' if turn == 0 else 'Yellow')} wins!!", 1, CYAN if turn == 0 else CYAN)
                        screen.blit(label, (50, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2  # Switch player

                    draw_board(board)
                    pygame.display.update()

                    if game_over:
                        pygame.time.wait(3000)  # Wait 3 seconds before closing

# Start the game
if __name__ == "__main__":
    draw_board(create_board())
    main()
    pygame.quit()
    sys.exit()