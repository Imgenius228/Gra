from objects import *
import database as db

finish = True
pause = False 
game = False
boss_round = False

# Функція для ініціалізації гри
def callback_start():
    global finish, player, enemys, game, scores, heal, level, coctail
    player = Player(player_image, 350, 250, 60, 60, 5)
    scores = 0
    heal = Bonus(heal_image, -100, -100, 40, 40)
    heal.spawn()
    level = 1
    coctail = Bonus(coctail_image, -100, -100, 50, 50)
    coctail.spawn()
    
    enemys.empty()
    for i in range(15):
        enemy = Enemy(zombie_images[0], 100, 100, 50, 50, 2)
        enemy.spawn()
        enemys.add(enemy)
    
    finish = False
    game = True

# Функція для виходу з гри
def callback_exit():
    exit()
    
# Створення кнопок
bt_start = Button(win_width / 2, 100, 100, 50, (50, 50, 100), bt_start_text, callback_start)
bt_exit = Button(win_width / 2, 400, 100, 50, (50, 50, 100), bt_exit_text, callback_exit)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
    if finish:
        bt_start.draw()
        bt_start.update() 
        bt_exit.draw()
        bt_exit.update()     
            
    elif game:
        win.blit(background, (0, 0))
        
        for enemy in enemys:
            dx = enemy.rect.centerx - player.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            ang = -math.atan2(dy, dx) - math.pi
            enemy.update(ang)
            enemy.draw()
            
            if player.hitbox.colliderect(enemy.hitbox):
                if enemy.max_hp == 15:
                    player.hp -= 20
                    enemy.kill()
                    boss_round = False
                else:
                    player.hp -= 10
                    enemy.spawn()
                   
        collide = pygame.sprite.groupcollide(bullets, enemys, True, False)
        if collide:
            enemy = list(collide.values())[0][0]
            enemy.hp -= 1
            if enemy.hp <= 0:
                if enemy.max_hp == 15:
                    scores += 5
                    enemy.kill()
                    boss_round = False
                else:
                    scores += 1
                    enemy.spawn()
        
        bullets.update()
        bullets.draw(win)
        
        player.update()
        player.draw()
        
        if scores % 15 == 0 and scores != 0 and not boss_round:
            boss = Enemy(zombie_images[0], - 100, -200, 120, 120, 2)
            boss.max_hp = 15
            boss.spawn()
            enemys.add(boss)
            boss_round = True
            
        if scores % 30 == 0 and scores != 0:
            scores += 1
            level += 1
            for enemy in enemys:
                if enemy.max_hp != 15:
                    enemy.max_hp += 1
                if level in (6, 9):
                    enemy.speed += 1
        
            if level >= 4:
                enemy = Enemy(zombie_images[0], 100, 100, 50, 50, 2)
                enemy.max_hp = level
                enemy.spawn()
                enemy.add(enemys)
        
        if player.hp <= 30:
            heal.draw()
            if player.hitbox.colliderect(heal.rect):
                player.hp += 30
                heal.spawn()
                
        if player.hp <= 70 and coctail.finish_effect():
            coctail.draw()
            if player.hitbox.colliderect(coctail.rect):
                coctail.start_effect(10)
                coctail.spawn()
                
        if not coctail.finish_effect():
            player.rate = 3
            player.speed = 6
        else:
            player.rate = 6
            player.speed = 5
        
        pygame.draw.rect(win, backgroun, UI)
        
        if player.hp <= 0:
            finish = True
            lose_text = ui_font.render("You died...", True, (255, 50, 50))
            win.blit(lose_text, (250, win_height + 5))
        
            db.add_result(scores)

            record = db.get_record()
            record_text = ui_font.render(f"The best result: {record}", True, (100, 100, 255))
            
            record_rect = record_text.get_rect(center=(win_width / 2, win_height - 50))
            
            win.blit(record_text, record_rect)
        else:
            level_text = ui_font.render(f"level: {level}", True, (200, 200, 200))
            win.blit(level_text, (250, win_height + 5))
        
        display_player_health(player)
        scores_text = ui_font.render(f"coins: {scores}", True, (255, 100, 100))
        win.blit(scores_text, (win_width - 180, win_height + 10))
    
    pygame.display.update()
    clock.tick(FPS)

