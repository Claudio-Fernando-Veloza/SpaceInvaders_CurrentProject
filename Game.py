import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_SPEED = 5
BULLET_SPEED = 7
BULLET_COOLDOWN = 500  # in milliseconds

# Alien settings
ALIEN_WIDTH, ALIEN_HEIGHT = 50, 50
ALIEN_SPEED = 1
ALIEN_SPAWN_INTERVAL = 20000  # in milliseconds
ALIEN_SPAWN_RATE = 1

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_img = pygame.image.load("images/JET.png")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
bullet_img = pygame.Surface((5, 15))
bullet_img.fill(WHITE)
alien_img = pygame.image.load("images/Alien.png")
alien_img = pygame.transform.scale(alien_img, (ALIEN_WIDTH, ALIEN_HEIGHT))

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = ALIEN_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = ALIEN_SPEED

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Variables for game loop
last_bullet_time = 0
last_alien_spawn_time = 0
game_over = False

while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if pygame.time.get_ticks() - last_bullet_time > BULLET_COOLDOWN:
                    player.shoot()
                    last_bullet_time = pygame.time.get_ticks()

    # Spawn aliens
    if pygame.time.get_ticks() - last_alien_spawn_time > ALIEN_SPAWN_INTERVAL:
        for _ in range(ALIEN_SPAWN_RATE):
            alien = Alien()
            all_sprites.add(alien)
            aliens.add(alien)
        last_alien_spawn_time = pygame.time.get_ticks()
        ALIEN_SPAWN_RATE *= 2

    # Update sprites
    all_sprites.update()

    # Check bullet-alien collisions
    hits = pygame.sprite.groupcollide(aliens, bullets, True, True)
    for hit in hits:
        pass  # You could add score here if you want

    # Check alien-player collisions
    if pygame.sprite.spritecollide(player, aliens, False):
        print("Game Over")
        game_over = True

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Flip display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()