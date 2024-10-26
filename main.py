from objects import *
from menu import Menu, HighScoreScreen
import database as db
import pygame
import random

def main():
    pygame.init()
    db.init_db()
    
    menu = Menu()
    high_scores = HighScoreScreen()
    current_screen = 'menu'
    running = True
    
    while running:
        if current_screen == 'menu':
            menu.draw(win)
            action = menu.handle_input()
            
            if action == 'start':
                current_screen = 'game'
                game_loop()
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

def game_loop():
    game_over = False
    score = 0
    level = 1
    player_name = "Player"  
    
    enemy_spawn_timer = pygame.time.get_ticks()
    current_time = enemy_spawn_timer
    
    player = PlayerTank(win_width//2 - TILE_SIZE//2, win_height - TILE_SIZE - 10)
    all_sprites.add(player)

    create_level(LEVEL_1)
    
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
                elif event.key == pygame.K_r and game_over:
                    return 'start'
        
        if not game_over:
            
            if current_time - enemy_spawn_timer > ENEMY_SPAWN_TIME and len(enemies) < 5:
                spawn_point = random.choice(ENEMY_SPAWN_POINTS)
                enemy = EnemyTank(spawn_point[0], spawn_point[1])
                enemies.add(enemy)
                all_sprites.add(enemy)
                enemy_spawn_timer = current_time
                
            all_sprites.update()
            
            
            for bullet in bullets:
                enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
                if enemy_hits:
                    score += 100
                    bullet.kill()
                    
                    
                    if random.random() < 0.2:  
                        bonus_type = random.choice(["speed", "star"])
                        bonus_image = BONUS_SPEED if bonus_type == "speed" else BONUS_STAR
                        bonus = Bonus(bonus_image, 
                                    enemy_hits[0].rect.x,
                                    enemy_hits[0].rect.y,
                                    bonus_type)
                        bonuses.add(bonus)
                        all_sprites.add(bonus)
                
                
                if pygame.sprite.collide_rect(bullet, player):
                    if bullet.dx != 0 or bullet.dy != 0:  
                        player.lives -= 1
                        bullet.kill()
                        if player.lives <= 0:
                            game_over = True
                            db.add_score(player_name, score, level)
            
            
            bonus_collected = pygame.sprite.spritecollide(player, bonuses, False)
            for bonus in bonus_collected:
                bonus.apply(player)
            
            
            if len(enemies) == 0 and current_time - enemy_spawn_timer > ENEMY_SPAWN_TIME:
                level += 1
                
        
        
        win.fill(BLACK)
        all_sprites.draw(win)
        
        
        score_text = game_font.render(f'Score: {score}', True, WHITE)
        lives_text = game_font.render(f'Lives: {player.lives}', True, WHITE)
        level_text = game_font.render(f'Level: {level}', True, WHITE)
        win.blit(score_text, (10, 10))
        win.blit(lives_text, (win_width - 100, 10))
        win.blit(level_text, (win_width//2 - 40, 10))
        
        if game_over:
            game_over_text = game_font.render('Game Over! Press R to restart', True, WHITE)
            win.blit(game_over_text, (win_width//2 - 100, win_height//2))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()