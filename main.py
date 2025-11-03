import pygame

# Window Set Up
pygame.init()
screen = pygame.display.set_mode((480, 720))
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.SysFont(None, 24)

# Global round and difficulty
current_round = 1
base_enemy_move_interval = 500
MAX_ROUND = 6

# Shooting delay and speed-up variables
shoot_delay = 150
speed_up_shown = False
speed_up_start_time = 0

# Initialize game state
def initialize_game(prev_score=0, round_num=1):
    global playerPos, health, player_alive, bullets, enemies, lastShot, last_enemy_move, score, game_over, game_win, enemy_move_interval, current_round, shoot_delay, speed_up_shown, speed_up_start_time
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

    current_round = min(round_num, MAX_ROUND)
    enemy_move_interval = max(100, base_enemy_move_interval - (current_round - 1) * 50)

    # Set shooting speed 
    if round_num == 4:
        shoot_delay = 75  # Faster shooting activated in round 4
        speed_up_shown = True
        speed_up_start_time = pygame.time.get_ticks()
    elif round_num == 6:
        shoot_delay = 50
        speed_up_shown = True
    elif round_num > 4:
        shoot_delay = 75  # Keep fast shooting
        speed_up_shown = False
    else:
        shoot_delay = 150  # Normal shooting speed before round 4
        speed_up_shown = False

    startenemies(current_round)

# Create centered enemies
def startenemies(round_num):
    rows = 3 + round_num
    cols = 5 + round_num
    spacing_x = 40
    spacing_y = 40

    block_width = (cols - 1) * spacing_x
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
    if currentTime - lastShot >= shoot_delay:
        bullets.append(pygame.Vector2(playerPos.x, playerPos.y))
        lastShot = currentTime

# Collision
def circle_collision(pos1, radius1, pos2, radius2):
    return pos1.distance_to(pos2) < (radius1 + radius2)

# Start first game
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
            initialize_game(0, 1)
        if game_win and current_round < MAX_ROUND and keys[pygame.K_n]:
            initialize_game(score, current_round + 1)

    screen.fill("black")

    # Score and round display
    score_text = font.render(f"Score: {score} | Round: {current_round}", True, (255, 0, 0))
    screen.blit(score_text, (screen.get_width() // 2 - 100, 10))

    if not game_over and not game_win:
        # Player input
        if player_alive:
            if keys[pygame.K_a] and playerPos.x > 52:
                playerPos.x -= 400 * dt
            if keys[pygame.K_d] and playerPos.x < 430:
                playerPos.x += 400 * dt
            if keys[pygame.K_SPACE]:
                shoot()

            pygame.draw.circle(screen, "purple", playerPos, 30)

        # Bullets
        for b in bullets[:]:
            b.y -= 500 * dt
            pygame.draw.circle(screen, "yellow", (b.x, b.y), 5)
            if b.y < 0:
                bullets.remove(b)

        # Enemy movement
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_move >= enemy_move_interval:
            for enemy in enemies:
                enemy.y += 20
            last_enemy_move = current_time

        # Bullet-enemy collision
        for b in bullets[:]:
            for enemy in enemies[:]:
                if circle_collision(b, 5, enemy, 20):
                    bullets.remove(b)
                    enemies.remove(enemy)
                    score += 10
                    break

        # Enemy-player collision
        if player_alive:
            for enemy in enemies[:]:
                if circle_collision(playerPos, 30, enemy, 20):
                    health -= 10
                    enemies.remove(enemy)

        # Player death
        if health <= 0 and player_alive:
            player_alive = False
            game_over = True

        # Win condition
        if not enemies:
            game_win = True

    # Draw enemies
    for enemy in enemies:
        pygame.draw.circle(screen, "green", enemy, 15)

    # Game Over Screen
    if game_over:
        game_over_text1 = font.render("Game Over", True, (255, 0, 0))
        game_over_text2 = font.render("Your Score was: " + str(score), True, (255, 0, 0))
        game_over_text3 = font.render("Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text1, (screen.get_width() // 2 - 75, screen.get_height() // 2 - 60))
        screen.blit(game_over_text2, (screen.get_width() // 2 - 75, screen.get_height() // 2 - 40))
        screen.blit(game_over_text3, (screen.get_width() // 2 - 75, screen.get_height() // 2 - 20))

    # Win Screen
    if game_win:
        if current_round >= MAX_ROUND:
            win_text1 = font.render("You Beat the Game!", True, (0, 255, 0))
            win_text2 = font.render("Final Score: " + str(score), True, (0, 255, 0))
            win_text3 = font.render("Press R to Restart", True, (0, 255, 0))
            screen.blit(win_text1, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 60))
            screen.blit(win_text2, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 40))
            screen.blit(win_text3, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 20))
        else:
            win_text1 = font.render("You Win This Round!", True, (255, 255, 0))
            win_text2 = font.render("Press N for Next Round", True, (255, 255, 0))
            win_text3 = font.render("Or Press R to Restart", True, (255, 255, 0))
            screen.blit(win_text1, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 60))
            screen.blit(win_text2, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 40))
            screen.blit(win_text3, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 20))

    # Show "Speed Up!" message for 2 seconds only in round 4
    if speed_up_shown:
        elapsed = pygame.time.get_ticks() - speed_up_start_time
        if elapsed <= 2000:
            speed_text = font.render("Speed Up!", True, (255, 255, 0))
            screen.blit(speed_text, (screen.get_width() // 2 - 50, 40))
        else:
            speed_up_shown = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
