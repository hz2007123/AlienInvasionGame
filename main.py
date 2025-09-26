import pygame
import time

# Window Set Up
pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
running = True
dt = 0

bullets = []

playerPos = pygame.Vector2(screen.get_width() / 2, 650) # Initial Player Starting Position
screenBorders = [52, 430]

moveSpeed = 400
bulletSpeed = 600

cooldown = 100
lastShot = 0

def shoot():
    global lastShot, cooldown
    currentTime = pygame.time.get_ticks()
    if currentTime - lastShot >= cooldown:
        bullets.append(pygame.Vector2(playerPos.x, playerPos.y))
        lastShot = currentTime

while running: # Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.draw.circle(screen, "purple", playerPos, 30)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and playerPos.x > screenBorders[0]:
        playerPos.x -= moveSpeed * dt
    if keys[pygame.K_d] and playerPos.x < screenBorders[1]:
        playerPos.x += moveSpeed * dt
    if keys[pygame.K_SPACE]:
        shoot()


    for b in bullets[:]:
        b.y -= bulletSpeed * dt
        pygame.draw.circle(screen, "yellow", (b.x, b.y), 5 )

        if b.y < 0:
            bullets.remove(b)



    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
