import pygame
import random 

def get_highscore(): 
    try: 
        with open("highscore.txt", "r") as f: 
            return int(f.read())
    except: 
        return 0

def write_highscore(score): 
    with open("highscore.txt", "w") as f: 
        f.write(str(score))

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
    def __init__(self, x=640):
        self.vel = -3
        self.x = x
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
        #Updating the highscore if needed
        highscore = get_highscore()
        if self.score > highscore: 
            highscore = self.score
            write_highscore(highscore)

        game_over_surface = pygame.font.SysFont(None, 72).render(f'Game Over! Score: {self.score}', True, (255, 0, 0))
        tooltip_surface = pygame.font.SysFont(None, 48).render(f'Press SPACE to Restart', True, (255, 0, 0))
        highscore_surface = pygame.font.SysFont(None, 48).render(f'High Score: {highscore}', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(320, 180))
        tooltip_rect = tooltip_surface.get_rect(center=(320, 240))
        highscore_rect = highscore_surface.get_rect(center=(320, 120))
        screen.blit(game_over_surface, game_over_rect)
        screen.blit(tooltip_surface, tooltip_rect)
        screen.blit(highscore_surface, highscore_rect)
