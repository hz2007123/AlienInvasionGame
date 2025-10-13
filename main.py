import pygame
import time

# Window Set Up
pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.SysFont(None, 32)

# Global round and difficulty
current_round = 1
base_enemy_move_interval = 500

# Initialize Variables
def initialize_game(prev_score=0, round_num=1):
    global playerPos, health, player_alive, bullets, enemies, lastShot, last_enemy_move, score
    global game_over, game_win, enemy_move_interval, current_round
    playerPos = pygame.Vector2(screen.get_width() / 2, 650)
    health = 30
    player_alive = True
    bullets = []
    enemies = []
    lastShot = 0
    last_enemy_move = 0
    score = prev_score
    game_over = False
    game_win = False
    current_round = round_num
    enemy_move_interval = max(100, base_enemy_move_interval - (round_num - 1) * 50)  # Increase speed every round
    startenemies(round_num)

# Create Enemies (scales with round)
def startenemies(round_num):
    rows = 3 + round_num  # More rows each round
    cols = 5 + round_num  # More columns each round
    spacing_x = 40  # horizontal gap at beginning
    spacing_y = 40  # vertical gap at beginning
    enemy_radius = 15

    # how much space enemies take up
    block_width = (cols - 1) * spacing_x

    # beginning x value to start in centre of screen
    start_x = (screen.get_width() - block_width) / 2

    for i in range(rows):
        y = 80 + i * spacing_y
        for j in range(cols):
            x = start_x + j * spacing_x
            enemies.append(pygame.Vector2(x, y))


# Shooting
def shoot():
    global lastShot
    currentTime = pygame.time.get_ticks()
    if currentTime - lastShot >= 150:
        bullets.append(pygame.Vector2(playerPos.x, playerPos.y))
        lastShot = currentTime

# Collision
def circle_collision(pos1, radius1, pos2, radius2):
    distance = pos1.distance_to(pos2)
    return distance < (radius1 + radius2)

# Start initial game
initialize_game()

# Game Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    # Restart or Next Round
    if game_over or game_win:
        if keys[pygame.K_r]:
            initialize_game(0, 1)  # Restart everything
        if game_win and keys[pygame.K_n]:
            initialize_game(score, current_round + 1)  # Start next round with carried score

    screen.fill("black")

    # Score Display
    score_counter = font.render(f"Score: {score} | Round: {current_round}", True, (255, 255, 255))
    screen.blit(score_counter, (screen.get_width() // 2 - 100, 10))

    if not game_over and not game_win:
        # Player Input
        if player_alive:
            if keys[pygame.K_a] and playerPos.x > 52:
                playerPos.x -= 400 * dt
            if keys[pygame.K_d] and playerPos.x < 430:
                playerPos.x += 400 * dt
            if keys[pygame.K_SPACE]:
                shoot()

            pygame.draw.circle(screen, "purple", playerPos, 30)

        # Update and Draw Bullets
        for b in bullets[:]:
            b.y -= 500 * dt
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
                    score += 10
                    break

        # Enemy-Player Collision
        if player_alive:
            for enemy in enemies[:]:
                if circle_collision(playerPos, 30, enemy, 20):
                    health -= 10
                    enemies.remove(enemy)

        # Player Death Check
        if health <= 0 and player_alive:
            player_alive = False
            game_over = True

        # Win Condition
        if not enemies:
            game_win = True

    # Draw Enemies
    for enemy in enemies:
        pygame.draw.circle(screen, "green", enemy, 15)

    # Game Over Screen
    if game_over:
        game_over_text1 = font.render("Game Over", True, (255, 0, 0))
        game_over_text2 = font.render(f"Your Score was: {score}", True, (255, 0, 0))
        game_over_text3 = font.render("Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text1, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 60))
        screen.blit(game_over_text2, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 40))
        screen.blit(game_over_text3, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 20))

    # Win Screen
    if game_win:
        win_text1 = font.render("You Win This Round!", True, (255, 255, 255))
        win_text2 = font.render(f"Current score: {score}", True, (255, 255, 255))
        win_text3 = font.render("Press N for Next Round", True, (255, 255, 255))
        win_text4 = font.render("Or Press R to Restart", True, (255, 255, 255))
        screen.blit(win_text1, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 80))
        screen.blit(win_text2, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 60))
        screen.blit(win_text3, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 40))
        screen.blit(win_text4, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 20))

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
