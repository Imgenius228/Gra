# Ініціалізація Pygame
import pygame
pygame.init()

# Розміри головного вікна та кадри в секунду
win_width = 1680
win_height = 920
FPS = 30

# Створення головного вікна
win = pygame.display.set_mode((win_width, win_height + 50))

# Створення годинника для контролю за частотою кадрів
clock = pygame.time.Clock()

# Завантаження шляхів до зображень для гравця, кулі та зомбі
player_image = "textures/player.png"
bullet_image = "textures/bullet.png"
zombie_images = ["textures/monster.png", "textures/monster1.png", "textures/monster2.png"]
heal_image = "textures/aptechka.png"
coctail_image = "textures/coctail.png"

# Завантаження та масштабування фонового зображення
background = pygame.transform.scale(pygame.image.load("textures/main_screen.png"), (win_width, win_height))

# Колір тла та інтерфейс внизу вікна
backgroun = (51, 255, 51)
UI = pygame.Rect(0, win_height, win_width, 50)

# Створення груп спрайтів для куль та ворогів
bullets = pygame.sprite.Group()
enemys = pygame.sprite.Group()

# Створення об'єкта шрифту для тексту інтерфейсу
ui_font = pygame.font.Font(None, 40)

# Текст для кнопок "Start" та "Exit"
bt_start_text = ui_font.render("Start", True, (100, 255, 255))
bt_exit_text = ui_font.render("Exit", True, (100, 255, 255))




