from objects import *
from menu import Menu, HighScoreScreen
import database as db
import pygame
import random
import sys

def initialize_game():
    """Инициализация игры и очистка всех групп спрайтов"""
    all_sprites.empty()
    walls.empty()
    bullets.empty()
    enemies.empty()
    bonuses.empty()
    
    pygame.init()
    db.init_db()
    return Menu(), HighScoreScreen()

def handle_bonus_collection(player, score):
    """Обработка подбора бонусов игроком"""
    bonus_collected = pygame.sprite.spritecollide(player, bonuses, False)
    for bonus in bonus_collected:
        bonus.apply(player)
    return score

def spawn_enemy_tank():
    """Попытка создать вражеский танк"""
    spawn_points = ENEMY_SPAWN_POINTS.copy()
    random.shuffle(spawn_points)
    
    for spawn_point in spawn_points:
        try:
            enemy = EnemyTank(spawn_point[0], spawn_point[1])
            # Проверяем, что танк не пересекается с другими объектами
            if not any(pygame.sprite.spritecollide(enemy, all_sprites, False)):
                enemies.add(enemy)
                all_sprites.add(enemy)
                return True
        except ValueError:
            continue
    return False

def handle_bullet_collisions(player, bullets, enemies, score, game_over):
    """Обработка столкновений пуль"""
    for bullet in bullets.sprites():  # Используем sprites() для безопасного перебора
        # Попадания по врагам (только пули игрока)
        if isinstance(bullet.owner, PlayerTank):
            enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemy_hits:
                score += 100
                bullet.kill()
                
                # Увеличиваем шанс появления бонуса и добавляем новые типы
                if random.random() < 0.3:  # Увеличили шанс с 0.2 до 0.3
                    bonus_type = random.choice(["speed", "star", "shield", "life"])
                    bonus_image = {
                        "speed": BONUS_SPEED,
                        "star": BONUS_STAR,
                        "shield": BONUS_SPEED,  # Замените на BONUS_SHIELD когда добавите изображение
                        "life": BONUS_STAR      # Замените на BONUS_LIFE когда добавите изображение
                    }[bonus_type]
                    
                    bonus = Bonus(
                        bonus_image,
                        enemy_hits[0].rect.x,
                        enemy_hits[0].rect.y,
                        bonus_type
                    )
                    bonuses.add(bonus)
                    all_sprites.add(bonus)
        
        # Попадания по игроку (только пули врагов)
        elif isinstance(bullet.owner, EnemyTank):
            if not player.invulnerable and pygame.sprite.collide_rect(bullet, player):
                player.lives -= 1
                player.make_invulnerable()
                bullet.kill()
                if player.lives <= 0:
                    game_over = True
    
    return score, game_over

def draw_game_interface(win, score, player, level, game_over, enemies_left):
    """Отрисовка игрового интерфейса"""
    # Отрисовка спрайтов
    win.fill(BLACK)
    all_sprites.draw(win)
    
    # Отрисовка текста
    score_text = game_font.render(f'Score: {score}', True, WHITE)
    lives_text = game_font.render(f'Lives: {player.lives}', True, WHITE)
    level_text = game_font.render(f'Level: {level}', True, WHITE)
    enemies_text = game_font.render(f'Enemies left: {enemies_left}', True, WHITE)
    
    win.blit(score_text, (10, 10))
    win.blit(lives_text, (win_width - 100, 10))
    win.blit(level_text, (win_width//2 - 40, 10))
    win.blit(enemies_text, (10, 40))
    
    if game_over:
        game_over_text = game_font.render('Game Over! Press R to restart', True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(win_width//2, win_height//2))
        win.blit(game_over_text, game_over_rect)
    
    pygame.display.flip()

def game_loop():
    """Основной игровой цикл"""
    # Инициализация игровых переменных
    initialize_game()
    game_over = False
    score = 0
    level = 1
    player_name = "Player"
    total_enemies_per_level = 10  # Общее количество врагов на уровень
    enemies_left = total_enemies_per_level  # Сколько врагов осталось создать
    enemies_defeated = 0  # Сколько врагов уничтожено
    
    # Создание игрока
    player = PlayerTank(win_width//2 - TILE_SIZE//2, win_height - TILE_SIZE - 10)
    all_sprites.add(player)
    
    # Создание уровня
    create_level(LEVEL_1)
    
    # Таймеры
    enemy_spawn_timer = pygame.time.get_ticks()
    level_start_time = pygame.time.get_ticks()
    
    while True:
        current_time = pygame.time.get_ticks()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
                elif event.key == pygame.K_r and game_over:
                    return 'start'
        
        if not game_over:
            # Создание врагов
            if (current_time - enemy_spawn_timer > ENEMY_SPAWN_TIME and 
                len(enemies) < 5 and 
                enemies_left > 0):
                if spawn_enemy_tank():
                    enemy_spawn_timer = current_time
                    enemies_left -= 1
            
            # Обновление всех спрайтов
            all_sprites.update()
            
            # Обработка столкновений
            old_enemy_count = len(enemies)
            score, game_over = handle_bullet_collisions(player, bullets, enemies, score, game_over)
            enemies_defeated += old_enemy_count - len(enemies)
            score = handle_bonus_collection(player, score)
            
            # Проверка условий перехода на следующий уровень
            if enemies_defeated >= total_enemies_per_level and len(enemies) == 0:
                level += 1
                enemies_left = total_enemies_per_level + (level - 1) * 2  # Увеличиваем количество врагов с каждым уровнем
                enemies_defeated = 0
                level_start_time = current_time
                
                # Увеличиваем сложность
                for enemy in enemies:
                    enemy.speed += 0.2  # Увеличиваем скорость врагов
                    enemy.shoot_chance += 0.01  # Увеличиваем частоту стрельбы
                
                # Добавляем бонусную жизнь при переходе на новый уровень
                if random.random() < 0.5:  # 50% шанс получить дополнительную жизнь
                    player.lives += 1
            
            # Сохранение результата при game over
            if game_over:
                db.add_score(player_name, score, level)
        
        # Отрисовка
        draw_game_interface(win, score, player, level, game_over, enemies_left + len(enemies))
        clock.tick(FPS)

def main():
    """Главная функция игры"""
    menu, high_scores = initialize_game()
    current_screen = 'menu'
    running = True
    
    while running:
        if current_screen == 'menu':
            menu.draw(win)
            action = menu.handle_input()
            
            if action == 'start':
                current_screen = 'game'
                result = game_loop()
                if result == 'exit':
                    running = False
                elif result == 'menu':
                    current_screen = 'menu'
            elif action == 'scores':
                current_screen = 'high_scores'
            elif action == 'exit':
                running = False
                
        elif current_screen == 'high_scores':
            scores = db.get_high_scores()
            high_scores.draw(win, scores)
            action = high_scores.handle_input()
            
            if action == 'menu':
                current_screen = 'menu'
            elif action == 'exit':
                running = False
                
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()