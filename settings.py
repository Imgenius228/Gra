import pygame
pygame.init()


win_width = 800
win_height = 600
TILE_SIZE = 40
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

TANK_PLAYER = "tank_player.png"
TANK_ENEMY = "tank_enemy.png"
BULLET = "bullet.png"
BRICK_WALL = "brick.png"
STEEL_WALL = "steel.png"
BONUS_SPEED = "speed.png"
BONUS_STAR = "star.png"

TANK_SPEED = 2       
BULLET_SPEED = 10     
ENEMY_SPAWN_TIME = 5000  

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

game_font = pygame.font.Font(None, 36)

LEVEL_1 = [
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,2],
    [2,0,2,2,0,0,1,0,0,2,2,0,0,1,0,0,2,2,0,2],
    [2,0,2,2,0,0,0,0,0,2,2,0,0,0,0,0,2,2,0,2],
    [2,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,2],
    [2,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,2],
    [2,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,2],
    [2,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,0,0,2],
    [2,0,0,0,0,0,1,0,1,2,2,1,0,1,0,0,0,0,0,2],
    [2,0,2,2,0,0,1,0,0,2,2,0,0,1,0,0,2,2,0,2],
    [2,0,2,2,0,0,1,0,0,0,0,0,0,1,0,0,2,2,0,2],
    [2,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,2],
    [2,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,2],
    [2,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,2],
    [2,2,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,2,2]
]

ENEMY_SPAWN_POINTS = [
    (TILE_SIZE * 2, 0),
    (win_width//2 - TILE_SIZE//2, 0),
    (win_width - TILE_SIZE * 3, 0)
]