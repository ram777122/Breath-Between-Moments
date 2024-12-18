import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ice Tower Inspired Game")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
PLAYER_SPEED = 5
JUMP_SPEED = -15
GRAVITY = 0.8

# Platform settings
PLATFORM_SPEED = 2
NUM_PLATFORMS = 6

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Generate starry background
STAR_COUNT = 100
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(STAR_COUNT)]

# Load images
player_image = pygame.image.load("player.png")
platform_image = pygame.image.load("platform.png")

# Scale images if necessary
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 10
platform_image = pygame.transform.scale(platform_image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))

# Functions
def draw_starry_background(surface):
    """Draw a starry background."""
    surface.fill(BLACK)
    for star in stars:
        pygame.draw.circle(surface, WHITE, star, 2)  # Draw small white circles as stars

def display_score(surface, score):
    """Display the score on the screen."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))

# Platform Class
class Platform(pygame.sprite.Sprite):
    def _init_(self, x, y, width=PLATFORM_WIDTH):
        super()._init_()
        self.image = pygame.transform.scale(platform_image, (width, PLATFORM_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, start_scrolling):
        if start_scrolling:
            self.rect.y += PLATFORM_SPEED
        if self.rect.top > HEIGHT:  # Remove platforms that go off-screen
            self.kill()

# Player Class
class Player(pygame.sprite.Sprite):
    def _init_(self, x, y):
        super()._init_()
        self.image = player_image
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity_y = 0
        self.can_jump = True  # Can jump when touching a platform
        self.jump_count = 0  # Track number of jumps

    def update(self, platforms):
        # Store previous position
        old_rect = self.rect.copy()

        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Reset jump state
        on_platform = False

        # Check for collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Landing on platform
                if self.velocity_y > 0 and old_rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    on_platform = True
                    self.can_jump = True
                    self.jump_count = 0  # Reset jump count when landing
                    break

        # Reset jump ability if not on platform
        if not on_platform:
            if self.jump_count >= 2:  # Limit to 2 jumps
                self.can_jump = False

        # Movement (left/right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def jump(self):
        # Allow jump if can jump and jump count is less than 2
        if self.can_jump and self.jump_count < 2:
            self.velocity_y = JUMP_SPEED
            self.jump_count += 1
            if self.jump_count >= 2:
                self.can_jump = False

    def check_fall(self):
        return self.rect.top > HEIGHT  # Game over if the player falls off the screen

# Main Game Function
def main():
    # Groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    # Generate the first full-width platform
    first_platform = Platform(0, HEIGHT - 50, WIDTH)
    all_sprites.add(first_platform)
    platforms.add(first_platform)

    # Generate initial small platforms above the first one
    for i in range(1, NUM_PLATFORMS):
        x = random.randint(0, WIDTH - PLATFORM_WIDTH)
        y = HEIGHT - 50 - i * (HEIGHT // NUM_PLATFORMS)
        platform = Platform(x, y)
        all_sprites.add(platform)
        platforms.add(platform)

    # Place the player on the first platform
    player = Player(WIDTH // 2, HEIGHT - 100)
    all_sprites.add(player)

    score = 0
    start_scrolling = False  # Flag to control screen scrolling
    running = True

    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()
                start_scrolling = True  # Start scrolling after the first jump

        # Update
        player.update(platforms)
        platforms.update(start_scrolling)

        # Add new platforms
        if len(platforms) < NUM_PLATFORMS:
            x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            y = -PLATFORM_HEIGHT
            platform = Platform(x, y)
            all_sprites.add(platform)
            platforms.add(platform)

        # Check Game Over
        if player.check_fall():
            running = False

        # Increase score after scrolling starts
        if start_scrolling:
            score += 1

        # Draw
        draw_starry_background(screen)  # Draw the starry background
        all_sprites.draw(screen)
        display_score(screen, score)

        # Refresh screen
        pygame.display.flip()
        clock.tick(FPS)

    # Game Over Screen
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 30))
    screen.blit(score_text, (WIDTH // 2 - 90, HEIGHT // 2 + 10))
    pygame.display.flip()
    pygame.time.wait(3000)

if _name_ == "_main_":
    main()
