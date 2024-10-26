import pygame
from settings import *
import random
import math

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
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
        self.original_image = self.image
        self.speed = TANK_SPEED
        self.shoot_delay = 500
        self.last_shot = 0
        self.lives = 3
        self.power_level = 1
        
    def move(self, dx, dy):
        old_x, old_y = self.rect.x, self.rect.y
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x, self.rect.y = old_x, old_y
            
        
        self.rect.clamp_ip(pygame.Rect(0, 0, win_width, win_height))
    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            dx = dy = 0
            if self.direction == 0:  
                dy = -1
                bullet_y = self.rect.top
                bullet_x = self.rect.centerx - 4 
            elif self.direction == 1: 
                dx = 1
                bullet_x = self.rect.right
                bullet_y = self.rect.centery - 4
            elif self.direction == 2:  
                dy = 1
                bullet_y = self.rect.bottom
                bullet_x = self.rect.centerx - 4
            elif self.direction == 3: 
                dx = -1
                bullet_x = self.rect.left
                bullet_y = self.rect.centery - 4
            
            bullet = Bullet(BULLET, bullet_x, bullet_y, dx, dy, self.power_level)
            bullets.add(bullet)
            all_sprites.add(bullet)

class PlayerTank(Tank):
    def __init__(self, x, y):
        super().__init__(TANK_PLAYER, x, y)
        self.lives = 3
        
    def update(self):
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
            self.shoot()
            
        self.move(dx, dy)
        self.rotate_to_direction()

class EnemyTank(Tank):
    def __init__(self, x, y):
        super().__init__(TANK_ENEMY, x, y)
        self.direction_change_time = random.randint(1000, 3000)
        self.last_direction_change = pygame.time.get_ticks()
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_direction_change > self.direction_change_time:
            self.direction = random.randint(0, 3)
            self.last_direction_change = now
            self.direction_change_time = random.randint(1000, 3000)
            
        dx = dy = 0
        if self.direction == 0: dy = -1
        elif self.direction == 1: dx = 1
        elif self.direction == 2: dy = 1
        elif self.direction == 3: dx = -1
            
        self.move(dx, dy)
        self.rotate_to_direction()
        
        if random.random() < 0.02:  
            self.shoot()

class Bullet(GameObject):
    def __init__(self, image_path, x, y, dx, dy, power):
        super().__init__(image_path, x, y)
        self.image = pygame.transform.scale(self.image, (6, 6)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy
        self.speed = BULLET_SPEED
        self.power = power
        
    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        
        
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()
            
        
        wall_hit = pygame.sprite.spritecollide(self, walls, False)
        if wall_hit:
            for wall in wall_hit:
                if isinstance(wall, BrickWall) or (isinstance(wall, SteelWall) and self.power > 1):
                    wall.kill()
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
        
    def apply(self, tank):
        if self.bonus_type == "speed":
            tank.speed += 1
        elif self.bonus_type == "star":
            tank.power_level += 1
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
