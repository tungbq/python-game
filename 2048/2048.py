import pygame
import sys
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 320
TILE_SIZE = 80
FONT_SIZE = 36
GRID_SIZE = 4
GRID_PADDING = 10
BACKGROUND_COLOR = GRAY
TILE_COLORS = {
    0: GRAY,
    2: YELLOW,
    4: ORANGE,
    8: RED,
    16: GREEN,
    32: BLUE,
    64: WHITE,
    128: GRAY,
    256: YELLOW,
    512: ORANGE,
    1024: RED,
    2048: GREEN
}

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")

# Font
font = pygame.font.SysFont(None, FONT_SIZE)

# Function to draw the grid
def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(screen, BLACK, (i * TILE_SIZE + GRID_PADDING, j * TILE_SIZE + GRID_PADDING, TILE_SIZE, TILE_SIZE), 5)

# Function to draw the tiles
def draw_tiles(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = board[i][j]
            tile_color = TILE_COLORS[tile_value]
            pygame.draw.rect(screen, tile_color, (i * TILE_SIZE + GRID_PADDING, j * TILE_SIZE + GRID_PADDING, TILE_SIZE, TILE_SIZE))
            if tile_value != 0:
                text_surface = font.render(str(tile_value), True, BLACK)
                text_rect = text_surface.get_rect(center=(i * TILE_SIZE + GRID_PADDING + TILE_SIZE // 2, j * TILE_SIZE + GRID_PADDING + TILE_SIZE // 2))
                screen.blit(text_surface, text_rect)

# Function to initialize the board
def initialize_board():
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Function to add a new tile to a random empty cell
def add_new_tile(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

# Function to move the tiles in a given direction
def move(board, direction):
    if direction == "up":
        board = [list(row) for row in zip(*board)]
        board = [move_row(row) for row in board]
        board = [list(row) for row in zip(*board)]
    elif direction == "down":
        board = [list(row[::-1]) for row in zip(*board)]
        board = [move_row(row) for row in board]
        board = [list(row[::-1]) for row in zip(*board)]
    elif direction == "left":
        board = [move_row(row) for row in board]
    elif direction == "right":
        board = [row[::-1] for row in board]
        board = [move_row(row) for row in board]
        board = [row[::-1] for row in board]
    return board

# Function to move a single row
def move_row(row):
    new_row = [0] * GRID_SIZE
    j = 0
    for i in range(GRID_SIZE):
        if row[i] != 0:
            if new_row[j] == 0:
                new_row[j] = row[i]
            elif new_row[j] == row[i]:
                new_row[j] *= 2
                j += 1
            else:
                j += 1
                new_row[j] = row[i]
    return new_row

# Function to check if the game is over
def is_game_over(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return False
            if i < GRID_SIZE - 1 and board[i][j] == board[i + 1][j]:
                return False
            if j < GRID_SIZE - 1 and board[i][j] == board[i][j + 1]:
                return False
    return True

# Function to check if the player has won
def has_won(board):
    for row in board:
        if 2048 in row:
            return True
    return False

# Main game loop
def main():
    board = initialize_board()
    add_new_tile(board)
    add_new_tile(board)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    board = move(board, "up")
                    add_new_tile(board)
                elif event.key == pygame.K_DOWN:
                    board = move(board, "down")
                    add_new_tile(board)
                elif event.key == pygame.K_LEFT:
                    board = move(board, "left")
                    add_new_tile(board)
                elif event.key == pygame.K_RIGHT:
                    board = move(board, "right")
                    add_new_tile(board)

        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_tiles(board)
        pygame.display.update()

        if has_won(board):
            print("Congratulations! You win!")
            break

        if is_game_over(board):
            print("Game over! You lose!")
            break

        pygame.time.delay(100)

# Run the game
if __name__ == "__main__":
    main()
