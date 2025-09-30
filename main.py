import pygame
import time

# Window Set Up
pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Player Setup
playerPos = pygame.Vector2(screen.get_width() / 2, 650)  # Initial Player Starting Position
screenBorders = [52, 430]
moveSpeed = 400

# Bullet Setup
bullets = []
bulletSpeed = 600
cooldown = 100
lastShot = 0

# Enemy Setup
enemies = []
enemy_radius = 20

# Create 6 enemies
for i in range(6):
    x = 60 + i * 70  # horizontal spacing
    y = 100          # vertical position
    enemies.append(pygame.Vector2(x, y))

# Shooting function
def shoot():
    global lastShot, cooldown
    currentTime = pygame.time.get_ticks()
    if currentTime - lastShot >= cooldown:
        bullets.append(pygame.Vector2(playerPos.x, playerPos.y))
        lastShot = currentTime

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and playerPos.x > screenBorders[0]:
        playerPos.x -= moveSpeed * dt
    if keys[pygame.K_d] and playerPos.x < screenBorders[1]:
        playerPos.x += moveSpeed * dt
    if keys[pygame.K_SPACE]:
        shoot()

    # Draw Player
    pygame.draw.circle(screen, "purple", playerPos, 30)

    # Update and Draw Bullets
    for b in bullets[:]:
        b.y -= bulletSpeed * dt
        pygame.draw.circle(screen, "yellow", (b.x, b.y), 5)

        if b.y < 0:
            bullets.remove(b)

    # Draw Enemies
    for enemy in enemies:
        pygame.draw.circle(screen, "green", enemy, enemy_radius)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
