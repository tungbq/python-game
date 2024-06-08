import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Function to draw the paddles
def draw_paddle(surface, x, y):
    pygame.draw.rect(surface, WHITE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Function to draw the ball
def draw_ball(surface, x, y):
    pygame.draw.circle(surface, WHITE, (x, y), BALL_RADIUS)

# Main game loop
def main():
    # Initialize paddle positions
    player_paddle_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2
    computer_paddle_y = (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2

    # Initialize ball position and velocity
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = BALL_SPEED_X * random.choice([-1, 1])
    ball_dy = BALL_SPEED_Y * random.choice([-1, 1])

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move player paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle_y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            player_paddle_y += PADDLE_SPEED

        # Ensure player paddle stays within bounds
        player_paddle_y = max(0, min(player_paddle_y, SCREEN_HEIGHT - PADDLE_HEIGHT))

        # Move computer paddle
        if ball_dy < 0:
            if computer_paddle_y > 0:
                computer_paddle_y -= PADDLE_SPEED
        else:
            if computer_paddle_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
                computer_paddle_y += PADDLE_SPEED

        # Move the ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Check for collisions with walls
        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
            ball_dy = -ball_dy

        # Check for collisions with paddles
        if (ball_x - BALL_RADIUS <= PADDLE_WIDTH and
            player_paddle_y <= ball_y <= player_paddle_y + PADDLE_HEIGHT):
            ball_dx = -ball_dx

        if (ball_x + BALL_RADIUS >= SCREEN_WIDTH - PADDLE_WIDTH and
            computer_paddle_y <= ball_y <= computer_paddle_y + PADDLE_HEIGHT):
            ball_dx = -ball_dx

        # Check for scoring
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            # Respawn ball
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_dx = BALL_SPEED_X * random.choice([-1, 1])
            ball_dy = BALL_SPEED_Y * random.choice([-1, 1])

        # Clear the screen
        screen.fill(BLACK)

        # Draw paddles and ball
        draw_paddle(screen, 0, player_paddle_y)
        draw_paddle(screen, SCREEN_WIDTH - PADDLE_WIDTH, computer_paddle_y)
        draw_ball(screen, ball_x, ball_y)

        # Update the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
