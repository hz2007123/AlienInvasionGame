import pygame
import time

# Window Set Up
pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.SysFont(None, 48)

# Initialize Variables
def initialize_game():
    global playerPos, health, player_alive, bullets, enemies, lastShot, last_enemy_move, score, game_over
    playerPos = pygame.Vector2(screen.get_width() / 2, 650)
    health = 30
    player_alive = True
    bullets = []
    enemies = []
    lastShot = 0
    last_enemy_move = 0
    score = 0
    game_over = False
    startenemies()

# Enemy Setup
enemy_move_interval = 750

# Create 6 enemies in 3 rows
def startenemies():
    for i in range(5):
        y = 100 + i * 50
        for j in range(8):
            x = 60 + j * 50
            enemies.append(pygame.Vector2(x, y))

def shoot():
    global lastShot
    currentTime = pygame.time.get_ticks()
    if currentTime - lastShot >= 200:
        bullets.append(pygame.Vector2(playerPos.x, playerPos.y))
        lastShot = currentTime

def circle_collision(pos1, radius1, pos2, radius2):
    distance = pos1.distance_to(pos2)
    return distance < (radius1 + radius2)

# Call to set initial game state after restart and on start
initialize_game()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    # Restart function
    if game_over:
        if keys[pygame.K_r]:
            initialize_game()

    screen.fill("black")

    if game_over != True:
        # Score Counter
        score_counter = font.render("Score: " + str(score), True, (255,0,0))
        screen.blit(score_counter, (screen.get_width() // 2 + 68.5, screen.get_height() // 2 - 330))
        # Player Input
        if player_alive:
            if keys[pygame.K_a] and playerPos.x > 52:
                playerPos.x -= 400 * dt
            if keys[pygame.K_d] and playerPos.x < 430:
                playerPos.x += 400 * dt
            if keys[pygame.K_SPACE]:
                shoot()

            # Draw Player
            pygame.draw.circle(screen, "purple", playerPos, 30)

        # Update and Draw Bullets
        for b in bullets[:]:
            b.y -= 600 * dt
            pygame.draw.circle(screen, "yellow", (b.x, b.y), 5)
            if b.y < 0:
                bullets.remove(b)

        # Enemy Movement
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_move >= enemy_move_interval:
            for enemy in enemies:
                enemy.y += 20
            last_enemy_move = current_time

        # Bullet-Enemy Collision
        for b in bullets[:]:
            for enemy in enemies[:]:
                if circle_collision(b, 5, enemy, 20):
                    bullets.remove(b)
                    enemies.remove(enemy)
                    score = score + 10
                    
                    break

        # Enemy-Player Collision
        if player_alive:
            for enemy in enemies[:]:
                if circle_collision(playerPos, 30, enemy, 20):
                    health -= 10
                    enemies.remove(enemy)

        # Check for Player Death
        if health <= 0 and player_alive:
            player_alive = False
            game_over = True

    # Draw Enemies
    for enemy in enemies:
        pygame.draw.circle(screen, "green", enemy, 15)

    # Game Over Screen
    if game_over:
        game_over_text1 = font.render("Game Over", True, (255, 0, 0))
        game_over_text2 = font.render("Your Score was: " + str(score), True, (255, 0, 0))
        game_over_text3 = font.render("Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text1, (40, screen.get_height() // 2 - 80))
        screen.blit(game_over_text2, (40, screen.get_height() // 2 - 50))
        screen.blit(game_over_text3, (40, screen.get_height() // 2 - 20))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
