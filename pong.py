import pygame
import random
import sys  # For clean exit

# --- 1. INITIALIZATION & SETUP ---
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 700, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game Settings
FPS = 60
PADDLE_SPEED = 6
SCORE_FONT = pygame.font.Font(None, 80)
CLOCK = pygame.time.Clock()


# --- 2. GAME OBJECT CLASSES ---

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 15
        self.height = 100
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.movement = 0  # -1 for up, 1 for down, 0 for stop

    def update(self):
        self.rect.y += self.movement * PADDLE_SPEED

        # Keep paddle within screen boundaries
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def move(self, direction):
        """Sets movement direction: -1 (up), 1 (down), 0 (stop)"""
        self.movement = direction


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 8
        self.image = pygame.Surface([self.radius * 2, self.radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.dx = self.speed * random.choice((1, -1))  # Start moving left or right
        self.dy = self.speed * random.choice((1, -1))  # Start moving up or down

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collision detection (top/bottom)
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1  # Reverse vertical direction

    def reset(self):
        """Resets ball position and reverses horizontal direction"""
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx *= -1
        self.dy = self.speed * random.choice((1, -1))  # Add some vertical randomness


# --- 3. HELPER FUNCTIONS ---

def draw_game(p1_score, p2_score):
    """Draws all elements on the screen."""
    SCREEN.fill(BLACK)

    # Draw scores
    p1_text = SCORE_FONT.render(str(p1_score), True, WHITE)
    p2_text = SCORE_FONT.render(str(p2_score), True, WHITE)
    SCREEN.blit(p1_text, (WIDTH // 4 - p1_text.get_width() // 2, 20))
    SCREEN.blit(p2_text, (WIDTH * 3 // 4 - p2_text.get_width() // 2, 20))

    # Draw center line
    pygame.draw.aaline(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw all sprites
    all_sprites.draw(SCREEN)

    pygame.display.flip()


def check_score(ball, p1_score, p2_score):
    """Checks if the ball went past a paddle and updates the score."""
    if ball.rect.left <= 0:
        p2_score += 1
        ball.reset()
    elif ball.rect.right >= WIDTH:
        p1_score += 1
        ball.reset()
    return p1_score, p2_score


def check_paddle_collision(ball, paddle):
    """Handles collision between the ball and a paddle."""
    if pygame.sprite.collide_rect(ball, paddle):
        # Only reverse dx if the ball is moving towards the paddle
        if (paddle.rect.centerx < WIDTH // 2 and ball.dx < 0) or \
                (paddle.rect.centerx > WIDTH // 2 and ball.dx > 0):
            ball.dx *= -1

            # Add small vertical change based on where the ball hit the paddle
            relative_y = ball.rect.centery - paddle.rect.centery
            # Normalize the hit position to a value between -1 and 1
            normalized_y = relative_y / (paddle.height / 2)

            # Adjust vertical direction based on hit point
            ball.dy = ball.speed * normalized_y


# --- 4. GAME OBJECT SETUP ---

# Create paddle objects
player1 = Paddle(30, HEIGHT // 2)
player2 = Paddle(WIDTH - 30, HEIGHT // 2)

# Create ball object
ball = Ball(WIDTH // 2, HEIGHT // 2)

# Create sprite group
all_sprites = pygame.sprite.Group(player1, player2, ball)

# Score variables
p1_score = 0
p2_score = 0


# --- 5. MAIN GAME LOOP ---

def main():
    global p1_score, p2_score  # Ensure we modify the global score variables

    running = True
    while running:
        # --- A. Event Handling (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle key presses (Paddle movement control)
            if event.type == pygame.KEYDOWN:
                # Player 1 (Left paddle) controls: W/S
                if event.key == pygame.K_w:
                    player1.move(-1)  # Move Up
                if event.key == pygame.K_s:
                    player1.move(1)  # Move Down

                # Player 2 (Right paddle) controls: Up/Down Arrows
                if event.key == pygame.K_UP:
                    player2.move(-1)  # Move Up
                if event.key == pygame.K_DOWN:
                    player2.move(1)  # Move Down

            if event.type == pygame.KEYUP:
                # Stop paddle movement when key is released
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.move(0)  # Stop
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2.move(0)  # Stop

        # --- B. Game Logic ---
        all_sprites.update()

        # Check collisions
        check_paddle_collision(ball, player1)
        check_paddle_collision(ball, player2)

        # Check scoring
        p1_score, p2_score = check_score(ball, p1_score, p2_score)

        # --- C. Drawing ---
        draw_game(p1_score, p2_score)

        # Control frame rate
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()