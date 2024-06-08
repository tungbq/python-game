import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)
GROUND_COLOR = (150, 100, 0)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
PIPE_WIDTH = 50
GAP_HEIGHT = 200
GRAVITY = 0.25
FLAP_HEIGHT = -6
BIRD_RADIUS = 20

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_HEIGHT

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, BIRD_COLOR, (self.x, int(self.y)), BIRD_RADIUS)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.min_gap = 100  # Minimum gap between pipes
        self.height = random.randint(50, SCREEN_HEIGHT - GAP_HEIGHT - self.min_gap - 50)
        self.passed = False

    def update(self):
        self.x -= 3

    def draw(self, screen):
        # Upper pipe
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
        # Lower pipe
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.height + self.min_gap, PIPE_WIDTH, SCREEN_HEIGHT))


class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over:
                        self.bird.flap()
                    else:
                        self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    if SCREEN_WIDTH // 2 - 50 < event.pos[0] < SCREEN_WIDTH // 2 + 50 and SCREEN_HEIGHT // 2 + 40 - 20 < event.pos[1] < SCREEN_HEIGHT // 2 + 40 + 20:
                        self.reset_game()


    def update(self):
        if not self.game_over:
            self.bird.update()
            if len(self.pipes) < 5:
                self.pipes.append(Pipe(SCREEN_WIDTH))
            for pipe in self.pipes:
                pipe.update()
                if pipe.x < self.bird.x and not pipe.passed:
                    self.score += 1
                    pipe.passed = True
                if pipe.x < -PIPE_WIDTH:
                    self.pipes.remove(pipe)
                # Adjust collision detection
                bird_x_left = self.bird.x - BIRD_RADIUS + 5  # Adjust the left side of the bird collider
                bird_x_right = self.bird.x + BIRD_RADIUS - 5  # Adjust the right side of the bird collider
                bird_y_top = self.bird.y - BIRD_RADIUS + 5  # Adjust the top side of the bird collider
                bird_y_bottom = self.bird.y + BIRD_RADIUS - 5  # Adjust the bottom side of the bird collider
                pipe_x_left = pipe.x + 5  # Adjust the left side of the pipe collider
                pipe_x_right = pipe.x + PIPE_WIDTH - 5  # Adjust the right side of the pipe collider
                pipe_top_y = pipe.height + 5  # Adjust the top side of the pipe collider
                pipe_bottom_y = pipe.height + GAP_HEIGHT - 5  # Adjust the bottom side of the pipe collider
                if (bird_y_top < pipe_top_y or bird_y_bottom > pipe_bottom_y) and pipe_x_left < bird_x_right and pipe_x_right > bird_x_left:
                    self.game_over = True


    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)
        self.draw_ground()
        self.draw_score()
        if self.game_over:
            self.draw_game_over()
        pygame.display.update()

    def draw_ground(self):
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        try_again_text = self.font.render("Try Again", True, (255, 255, 255))
        try_again_rect = try_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        pygame.draw.rect(self.screen, (0, 0, 255), try_again_rect)
        self.screen.blit(try_again_text, try_again_rect)

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
