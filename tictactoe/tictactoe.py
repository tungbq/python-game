import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 350  # Extra space for the reset button
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(WHITE)

# Board
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Draw grid lines
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

# Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_winner(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            draw_winning_line(row, 0, row, BOARD_COLS - 1)
            return True

    # Check columns
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            draw_winning_line(0, col, BOARD_ROWS - 1, col)
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        draw_winning_line(0, 0, BOARD_ROWS - 1, BOARD_COLS - 1)
        return True
    if all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        draw_winning_line(0, BOARD_COLS - 1, BOARD_ROWS - 1, 0)
        return True

    return False

def draw_winning_line(start_row, start_col, end_row, end_col):
    start_x = start_col * SQUARE_SIZE + SQUARE_SIZE // 2
    start_y = start_row * SQUARE_SIZE + SQUARE_SIZE // 2
    end_x = end_col * SQUARE_SIZE + SQUARE_SIZE // 2
    end_y = end_row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y), LINE_WIDTH)

def draw_reset_button():
    pygame.draw.rect(screen, BUTTON_COLOR, (WIDTH // 4, HEIGHT - 45, WIDTH // 2, 40))
    font = pygame.font.Font(None, 36)
    text = font.render('Reset', True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))

def reset_button_hover():
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (WIDTH // 4, HEIGHT - 45, WIDTH // 2, 40))
    font = pygame.font.Font(None, 36)
    text = font.render('Reset', True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 40))

def restart():
    screen.fill(WHITE)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None
    draw_reset_button()

# Main game loop
player = 'X'
game_over = False

draw_reset_button()
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if HEIGHT - 50 < mouse_y < HEIGHT - 10 and WIDTH // 4 < mouse_x < 3 * WIDTH // 4:
                restart()
                player = 'X'
                game_over = False
            elif not game_over:
                clicked_row = mouse_y // SQUARE_SIZE
                clicked_col = mouse_x // SQUARE_SIZE

                if clicked_row < BOARD_ROWS and available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_winner(player):
                        game_over = True
                    player = 'O' if player == 'X' else 'X'
                    draw_figures()

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if HEIGHT - 50 < mouse_y < HEIGHT - 10 and WIDTH // 4 < mouse_x < 3 * WIDTH // 4:
                reset_button_hover()
            else:
                draw_reset_button()

    pygame.display.update()
