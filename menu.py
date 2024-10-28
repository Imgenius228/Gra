import pygame
from settings import *

class Menu:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ['Start Game', 'High Scores', 'Exit']
        
    def draw(self, surface):
        surface.fill(BLACK)
        
       
        title = self.font_big.render('BATTLE CITY', True, WHITE)
        title_rect = title.get_rect(center=(win_width//2, 100))
        surface.blit(title, title_rect)
        
        
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected_option else WHITE
            text = self.font_small.render(option, True, color)
            text_rect = text.get_rect(center=(win_width//2, 300 + i * 60))
            surface.blit(text, text_rect)
            
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        return 'start'
                    elif self.selected_option == 1:
                        return 'scores'
                    elif self.selected_option == 2:
                        return 'exit'
        return None

class HighScoreScreen:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 48)
        self.font_scores = pygame.font.Font(None, 36)
        
    def draw(self, surface, scores):
        surface.fill(BLACK)
        
        
        title = self.font_title.render('HIGH SCORES', True, WHITE)
        title_rect = title.get_rect(center=(win_width//2, 50))
        surface.blit(title, title_rect)
        
        
        for i, (name, score, level, date) in enumerate(scores):
            text = self.font_scores.render(
                f'{i+1}. {name}: {score} (Level {level})', 
                True, 
                WHITE
            )
            text_rect = text.get_rect(x=100, y=120 + i * 40)
            surface.blit(text, text_rect)
            
        
        back_text = self.font_scores.render('Press ESC to return', True, WHITE)
        back_rect = back_text.get_rect(center=(win_width//2, win_height - 50))
        surface.blit(back_text, back_rect)
        
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
        return None
    

class GameOverScreen:
    def __init__(self):
        self.font_big = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ['Try Again', 'Main Menu']
        
    def draw(self, surface, score, level):
        surface.fill(BLACK)
        
        title = self.font_big.render('GAME OVER', True, WHITE)
        title_rect = title.get_rect(center=(win_width//2, 100))
        surface.blit(title, title_rect)
        
        score_text = self.font_small.render(f'Score: {score}', True, WHITE)
        score_rect = score_text.get_rect(center=(win_width//2, 200))
        surface.blit(score_text, score_rect)
        
        level_text = self.font_small.render(f'Level: {level}', True, WHITE)
        level_rect = level_text.get_rect(center=(win_width//2, 240))
        surface.blit(level_text, level_rect)
        
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected_option else WHITE
            text = self.font_small.render(option, True, color)
            text_rect = text.get_rect(center=(win_width//2, 350 + i * 60))
            surface.blit(text, text_rect)
            
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'exit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0: 
                        return 'retry'
                    elif self.selected_option == 1: 
                        return 'menu'
        return None
