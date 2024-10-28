import pygame
from settings import *
import random
import math

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 0  
        
    def rotate_to_direction(self):
        self.image = pygame.transform.rotate(self.original_image, -90 * self.direction)
        self.rect = self.image.get_rect(center=self.rect.center)

class Tank(GameObject):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)
        self.speed = TANK_SPEED
        self.shoot_delay = 500  
        self.last_shot = 0
        self.lives = 3
        self.power_level = 1
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 2000  
        
    def make_invulnerable(self):
        self.invulnerable = True
        self.invulnerable_timer = pygame.time.get_ticks()
        
    def update_invulnerability(self):
        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_timer > self.invulnerable_duration:
            self.invulnerable = False
            
    def handle_collision(self):
        wall_hits = pygame.sprite.spritecollide(self, walls, False)
        if wall_hits:
            return True
            
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(self.rect):
            return True
            
        return False
        
    def move(self, dx, dy):
        old_x, old_y = self.rect.x, self.rect.y
        
        self.rect.x += dx * self.speed
        if self.handle_collision():
            self.rect.x = old_x

        self.rect.y += dy * self.speed
        if self.handle_collision():
            self.rect.y = old_y
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            dx = dy = 0
            if self.direction == 0: 
                dy = -1
                bullet_x = self.rect.centerx
                bullet_y = self.rect.top
            elif self.direction == 1:
                dx = 1
                bullet_x = self.rect.right
                bullet_y = self.rect.centery
            elif self.direction == 2:  
                dy = 1
                bullet_x = self.rect.centerx
                bullet_y = self.rect.bottom
            else: 
                dx = -1
                bullet_x = self.rect.left
                bullet_y = self.rect.centery
            
            if 'SOUND_SHOOT' in globals():
                SOUND_SHOOT.play()
                
            bullet = Bullet(BULLET, bullet_x, bullet_y, dx, dy, self.power_level, self)
            return bullet
        return None

class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(TANK_PLAYER, x, y)
        self.lives = 3
        self.score = 0
        self.respawn_point = (x, y)
        
    def respawn(self):
        self.rect.x, self.rect.y = self.respawn_point
        self.direction = 0
        self.rotate_to_direction()
        self.make_invulnerable()
        
    def update(self):
        self.update_invulnerability()
        
        keys = pygame.key.get_pressed()
        dx = dy = 0
        
        if keys[pygame.K_w]:
            self.direction = 0
            dy = -1
        elif keys[pygame.K_s]:
            self.direction = 2
            dy = 1
        elif keys[pygame.K_a]:
            self.direction = 3
            dx = -1
        elif keys[pygame.K_d]:
            self.direction = 1
            dx = 1
            
        if keys[pygame.K_SPACE]:
            bullet = self.shoot()
            if bullet:
                bullets.add(bullet)
                all_sprites.add(bullet)
                
        self.move(dx, dy)
        self.rotate_to_direction()

class EnemyTank(Tank):
    def __init__(self, x, y):
        super().__init__(TANK_ENEMY, x, y)
        self.direction_change_time = random.randint(1000, 3000)
        self.last_direction_change = pygame.time.get_ticks()
        self.shoot_chance = 0.02
        
        # Проверяем начальную позицию
        if not self.is_valid_position(x, y):
            raise ValueError("Invalid spawn position")
            
    def is_valid_position(self, x, y):
        temp_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        
        for wall in walls:
            if temp_rect.colliderect(wall.rect):
                return False
                
        for sprite in all_sprites:
            if isinstance(sprite, Tank) and sprite.rect.colliderect(temp_rect):
                return False
                
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(temp_rect):
            return False
            
        return True
        
    def think(self):
        now = pygame.time.get_ticks()
        
        if now - self.last_direction_change > self.direction_change_time:
            self.direction = random.randint(0, 3)
            self.last_direction_change = now
            self.direction_change_time = random.randint(1000, 3000)
            

        if random.random() < self.shoot_chance:
            bullet = self.shoot()
            if bullet:
                bullets.add(bullet)
                all_sprites.add(bullet)
    
    def update(self):
        self.think()
        
        dx = dy = 0
        if self.direction == 0: dy = -1
        elif self.direction == 1: dx = 1
        elif self.direction == 2: dy = 1
        elif self.direction == 3: dx = -1
            
        self.move(dx, dy)
        self.rotate_to_direction()

class Bullet(GameObject):
    def __init__(self, image_path, x, y, dx, dy, power, owner):
        super().__init__(image_path, x, y)
        self.image = pygame.transform.scale(self.image, (8, 8))
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy
        self.speed = BULLET_SPEED
        self.power = power
        self.owner = owner
        
    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()
            return
            
        wall_hit = pygame.sprite.spritecollide(self, walls, False)
        if wall_hit:
            for wall in wall_hit:
                if isinstance(wall, BrickWall):  
                    wall.kill()
                    if 'SOUND_EXPLOSION' in globals():
                        SOUND_EXPLOSION.play()
                elif isinstance(wall, SteelWall) and self.power > 1:  
                    wall.kill()
                    if 'SOUND_EXPLOSION' in globals():
                        SOUND_EXPLOSION.play()
            self.kill()

class Wall(GameObject):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, x, y)

class BrickWall(Wall):
    def __init__(self, x, y):
        super().__init__(BRICK_WALL, x, y)

class SteelWall(Wall):
    def __init__(self, x, y):
        super().__init__(STEEL_WALL, x, y)

class Bonus(GameObject):
    def __init__(self, image_path, x, y, bonus_type):
        super().__init__(image_path, x, y)
        self.bonus_type = bonus_type
        self.duration = 10000  

    def apply(self, tank):
        if self.bonus_type == "speed":
            tank.speed += 1
        elif self.bonus_type == "star":
            tank.power_level = min(tank.power_level + 1, 3)
        elif self.bonus_type == "shield":
            tank.make_invulnerable()
            tank.invulnerable_duration = 5000  
        elif self.bonus_type == "life":
            tank.lives += 1
        self.kill()
        
    def apply(self, tank):
        if self.bonus_type == "speed":
            tank.speed += 1
        elif self.bonus_type == "star":
            tank.power_level = min(tank.power_level + 1, 3)  
        elif self.bonus_type == "shield":
            tank.make_invulnerable()
        self.kill()

def create_level(level_map):
    for row_index, row in enumerate(level_map):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if cell == 1:
                wall = BrickWall(x, y)
                walls.add(wall)
                all_sprites.add(wall)
            elif cell == 2:
                wall = SteelWall(x, y)
                walls.add(wall)
                all_sprites.add(wall)

def spawn_enemy(spawn_points):
    random.shuffle(spawn_points)
    for x, y in spawn_points:
        try:
            enemy = EnemyTank(x, y)
            enemies.add(enemy)
            all_sprites.add(enemy)
            return True
        except ValueError:
            continue
    return False