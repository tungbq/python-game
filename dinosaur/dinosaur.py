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
OBSTACLE_SPEED = 7
GRAVITY = 1
JUMP_HEIGHT = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DINO_COLOR = (0, 255, 0)  # Green color for dinosaur
OBSTACLE_COLOR = (255, 0, 0)  # Red color for obstacle

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
    pygame.draw.rect(screen, DINO_COLOR, (x, y - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT))

# Function to draw obstacles
def draw_obstacle(x, y):
    pygame.draw.rect(screen, OBSTACLE_COLOR, (x, y - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Function to display text
def display_text(text, x, y):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to check if the mouse is over a rectangle
def is_mouse_over(rect):
    mouse_pos = pygame.mouse.get_pos()
    return rect.collidepoint(mouse_pos)

# Main game loop
def main():
    # Initialize game variables
    dino_x = 50
    dino_y = SCREEN_HEIGHT - GROUND_HEIGHT - DINO_HEIGHT
    dino_dy = 0
    is_jumping = False
    obstacle_x = SCREEN_WIDTH
    obstacle_y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT  # Start obstacle at ground level
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
            if event.type == pygame.MOUSEBUTTONDOWN and is_game_over:
                if is_mouse_over(try_again_rect):
                    # Reset game variables
                    obstacle_x = SCREEN_WIDTH
                    obstacle_y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT  # Align obstacle with ground
                    score = 0
                    is_game_over = False

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
                obstacle_y = SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT  # Align obstacle with ground
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

        # Display game over message and try again button
        if is_game_over:
            display_text("Game Over", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            try_again_text = "Try Again"
            try_again_width, try_again_height = font.size(try_again_text)
            try_again_rect = pygame.Rect(
                (SCREEN_WIDTH - try_again_width) // 2,
                (SCREEN_HEIGHT - try_again_height) // 2 + 20,
                try_again_width,
                try_again_height
            )
            pygame.draw.rect(screen, WHITE, try_again_rect, 2)
            display_text(try_again_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)

        # Update the display
        pygame.display.update()

        # Frame rate
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
