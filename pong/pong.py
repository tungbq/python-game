import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
DINO_WIDTH = 40
DINO_HEIGHT = 40
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
OBSTACLE_SPEED = 5
GRAVITY = 1
JUMP_HEIGHT = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Font
font = pygame.font.SysFont(None, 30)

# Function to draw the ground
def draw_ground():
    pygame.draw.rect(screen, WHITE, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

# Function to draw the dinosaur
def draw_dinosaur(x, y):
    pygame.draw.rect(screen, WHITE, (x, y - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT))

# Function to draw obstacles
def draw_obstacle(x, y):
    pygame.draw.rect(screen, WHITE, (x, y - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Function to display text
def display_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Main game loop
def main():
    # Initialize game variables
    dino_x = 50
    dino_y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
    dino_dy = 0
    is_jumping = False
    obstacle_x = SCREEN_WIDTH
    obstacle_y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT
    score = 0
    is_game_over = False

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping and not is_game_over:
                    is_jumping = True
                    dino_dy = -JUMP_HEIGHT

        # Update dinosaur position
        if is_jumping:
            dino_y += dino_dy
            dino_dy += GRAVITY
            if dino_y >= SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT:
                dino_y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
                is_jumping = False

        # Update obstacle position
        if not is_game_over:
            obstacle_x -= OBSTACLE_SPEED
            if obstacle_x + OBSTACLE_WIDTH < 0:
                obstacle_x = SCREEN_WIDTH
                obstacle_y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(100, 300) # Randomize obstacle height
                score += 1

        # Check for collision
        dino_rect = pygame.Rect(dino_x, dino_y - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        if dino_rect.colliderect(obstacle_rect):
            is_game_over = True

        # Clear the screen
        screen.fill(BLACK)

        # Draw the ground
        draw_ground()

        # Draw the dinosaur
        draw_dinosaur(dino_x, dino_y)

        # Draw the obstacle
        draw_obstacle(obstacle_x, obstacle_y)

        # Display score
        display_text(f"Score: {score}", SCREEN_WIDTH // 2, 30)

        # Display game over message
        if is_game_over:
            display_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Update the display
        pygame.display.update()

        # Frame rate
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
