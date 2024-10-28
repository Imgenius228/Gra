from objects import *
from menu import Menu, HighScoreScreen, GameOverScreen
import database as db
import pygame
import random
import sys

def initialize_game():
    all_sprites.empty()
    walls.empty()
    bullets.empty()
    enemies.empty()
    bonuses.empty()
    
    pygame.init()
    db.init_db()
    return Menu(), HighScoreScreen(), GameOverScreen()

def initialize_game():
    all_sprites.empty()
    walls.empty()
    bullets.empty()
    enemies.empty()
    bonuses.empty()
    
    pygame.init()
    pygame.mixer.init()  
    
    global shoot_sound, explosion_sound, bonus_sound
    try:
        shoot_sound = pygame.mixer.Sound(SOUND_SHOOT)
        explosion_sound = pygame.mixer.Sound(SOUND_EXPLOSION)
        bonus_sound = pygame.mixer.Sound(SOUND_BONUS)
        
        shoot_sound.set_volume(0.3)
        explosion_sound.set_volume(0.4)
        bonus_sound.set_volume(0.5)
    except:
        print("Не удалось загрузить звуковые файлы")
    
    db.init_db()
    return Menu(), HighScoreScreen(), GameOverScreen()

def play_music(music_file, loop=True):
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1 if loop else 0)
    except:
        print(f"Не удалось загрузить музыку: {music_file}")

class GameState:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.player_name = "Player"
        self.total_enemies_per_level = 10
        self.enemies_left = self.total_enemies_per_level
        self.enemies_defeated = 0
        self.game_over = False
        self.player = None
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.level_start_time = pygame.time.get_ticks()

    def reset(self):
        self.__init__()
        self.player = PlayerTank(win_width//2 - TILE_SIZE//2, win_height - TILE_SIZE - 10)
        all_sprites.add(self.player)
        create_level(LEVEL_1)

def handle_bonus_collection(player, score):
    bonus_collected = pygame.sprite.spritecollide(player, bonuses, False)
    for bonus in bonus_collected:
        bonus.apply(player)
    return score

def spawn_enemy_tank():
    spawn_points = ENEMY_SPAWN_POINTS.copy()
    random.shuffle(spawn_points)
    
    for spawn_point in spawn_points:
        try:
            enemy = EnemyTank(spawn_point[0], spawn_point[1])
            if not any(pygame.sprite.spritecollide(enemy, all_sprites, False)):
                enemies.add(enemy)
                all_sprites.add(enemy)
                return True
        except ValueError:
            continue
    return False

def handle_bullet_collisions(game_state):
    for bullet in bullets.sprites():
        if isinstance(bullet.owner, PlayerTank):
            enemy_hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemy_hits:
                game_state.score += 100
                bullet.kill()
                
                if random.random() < 0.3:
                    bonus_type = random.choice(["speed", "star", "shield", "life"])
                    bonus_image = {
                        "speed": BONUS_SPEED,
                        "star": BONUS_STAR,
                        "shield": BONUS_SPEED,
                        "life": BONUS_STAR
                    }[bonus_type]
                    
                    bonus = Bonus(
                        bonus_image,
                        enemy_hits[0].rect.x,
                        enemy_hits[0].rect.y,
                        bonus_type
                    )
                    bonuses.add(bonus)
                    all_sprites.add(bonus)
        
        elif isinstance(bullet.owner, EnemyTank):
            if not game_state.player.invulnerable and pygame.sprite.collide_rect(bullet, game_state.player):
                game_state.player.lives -= 1
                game_state.player.make_invulnerable()
                bullet.kill()
                if game_state.player.lives <= 0:
                    game_state.game_over = True
                    return 'game_over'
    return None

def draw_game_interface(win, game_state):
    win.fill(BLACK)
    all_sprites.draw(win)
    
    score_text = game_font.render(f'Score: {game_state.score}', True, WHITE)
    lives_text = game_font.render(f'Lives: {game_state.player.lives}', True, WHITE)
    level_text = game_font.render(f'Level: {game_state.level}', True, WHITE)
    enemies_text = game_font.render(f'Enemies left: {game_state.enemies_left + len(enemies)}', True, WHITE)
    
    win.blit(score_text, (10, 10))
    win.blit(lives_text, (win_width - 100, 10))
    win.blit(level_text, (win_width//2 - 40, 10))
    win.blit(enemies_text, (10, 40))
    
    pygame.display.flip()

def game_loop(game_state):
    while True:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
        
        if not game_state.game_over:
            if (current_time - game_state.enemy_spawn_timer > ENEMY_SPAWN_TIME and 
                len(enemies) < 5 and 
                game_state.enemies_left > 0):
                if spawn_enemy_tank():
                    game_state.enemy_spawn_timer = current_time
                    game_state.enemies_left -= 1
            
            all_sprites.update()
            
            old_enemy_count = len(enemies)
            result = handle_bullet_collisions(game_state)
            if result == 'game_over':
                return 'game_over'
                
            game_state.enemies_defeated += old_enemy_count - len(enemies)
            game_state.score = handle_bonus_collection(game_state.player, game_state.score)
            
            if game_state.enemies_defeated >= game_state.total_enemies_per_level and len(enemies) == 0:
                game_state.level += 1
                game_state.enemies_left = game_state.total_enemies_per_level + (game_state.level - 1) * 2
                game_state.enemies_defeated = 0
                game_state.level_start_time = current_time
                
                for enemy in enemies:
                    enemy.speed += 0.2
                    enemy.shoot_chance += 0.01
                
                if random.random() < 0.5:
                    game_state.player.lives += 1
            
            draw_game_interface(win, game_state)
            clock.tick(FPS)

def main():
    menu, high_scores, game_over_screen = initialize_game()
    game_state = GameState()
    current_screen = 'menu'
    running = True
    play_music(MUSIC_MENU)


    while running:
        if current_screen == 'menu':
            menu.draw(win)
            action = menu.handle_input()
            
            if action == 'start':
                game_state.reset()
                play_music(MUSIC_GAME)
                current_screen = 'game'
            elif action == 'scores':
                current_screen = 'high_scores'
            elif action == 'exit':
                running = False
                
        elif current_screen == 'game':
            result = game_loop(game_state)
            if result == 'exit':
                running = False
            elif result == 'menu':
                current_screen = 'menu'
            elif result == 'game_over':
                db.add_score(game_state.player_name, game_state.score, game_state.level)
                current_screen = 'game_over'
                
        elif current_screen == 'high_scores':
            scores = db.get_high_scores()
            high_scores.draw(win, scores)
            action = high_scores.handle_input()
            
            if action == 'menu':
                current_screen = 'menu'
            elif action == 'exit':
                running = False
                
        elif current_screen == 'game_over':
            play_music(MUSIC_MENU)
            game_over_screen.draw(win, game_state.score, game_state.level)
            action = game_over_screen.handle_input()
            
            if action == 'retry':
                game_state.reset()
                current_screen = 'game'
            elif action == 'menu':
                current_screen = 'menu'
            elif action == 'exit':
                running = False
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()