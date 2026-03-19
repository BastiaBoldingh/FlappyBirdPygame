import pygame
import random 

class Bird: 
    def __init__(self, x, y): 
        self.x = x
        self.y = y
        self.vel_y = 0
        self.gravity = 0.5
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.image.fill((255, 0, 0))
    
    def update(self): 
        #Apply gravity
        if self.vel_y < 10: 
            self.vel_y += self.gravity
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y)
    
    def flap(self):
        self.vel_y = -8
    
    def draw(self, screen): 
        screen.blit(self.image, self.rect)

class Pipe:
    def __init__(self):
        self.vel = -3
        self.x = 640
        self.width = 50
        self.gap = 150
        self.top_height = random.randint(50, 200)
        self.bottom_height = 360 - self.top_height - self.gap
        self.color = (0, 255, 0)
        self.passed = False

    def update(self, speed_multiplier):
        self.x += self.vel *speed_multiplier

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, self.color, (self.x, 360 - self.bottom_height, self.width, self.bottom_height))
    

class ScoreBoard:
    def __init__(self):
        self.score = 0
        self.text_surface = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(topleft=(10, 10))
    def increment(self):
        self.score += 1
    
    def draw_score(self, screen):
        self.text_surface = pygame.font.SysFont(None, 36).render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(self.text_surface, self.text_rect)
    
    def draw_game_over(self, screen):
        game_over_surface = pygame.font.SysFont(None, 72).render('Game Over!', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(320, 180))
        screen.blit(game_over_surface, game_over_rect)
