import pygame
import sys
from entities import Bird, Pipe, ScoreBoard
from button import Button
from background import BackgroundObject
import os


pygame.init()

icon = pygame.surface.Surface((10, 10))
icon.fill((255, 0, 0))

pygame.display.set_icon(icon)
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 360
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60

# Render to a fixed internal surface then scale to window size for resize support
game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

BACKGROUND_IMG = pygame.image.load(os.path.join('assets', 'images', 'flappy_bird_background.png')).convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (WINDOW_WIDTH, 300))
FLOOR_IMG = pygame.image.load(os.path.join('assets', 'images', 'flappy_bird_floor.png')).convert()



running = True

def draw_text(screen, text, size, color, x, y, font):
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect) 

def new_game():
    global screen
    bird = Bird(100, 180)
    pipes = [Pipe(), Pipe(x=960)]
    scoreboard = ScoreBoard()
    background = BackgroundObject(BACKGROUND_IMG, speed=1)
    floor = BackgroundObject(FLOOR_IMG, speed=3, y=300)
    counter = 0
    speed_multiplier = 1.0


    game_over = False
    game_on = True
    bird.flap()
    while game_on:
        speed_multiplier = 1 + scoreboard.score * 0.01
        background.update()
        floor.update(speed_multiplier=speed_multiplier)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.flap()
        # Drawing background            
        game_surface.fill((255, 255, 255))
        background.draw(game_surface)
        floor.draw(game_surface)

        # Updating and drawing entities
        bird.update()
        bird.draw(game_surface)

        for pipe in pipes:
            pipe.update(speed_multiplier=speed_multiplier)
            pipe.draw(game_surface)
            if pipe.x < 100 and not pipe.passed: 
                scoreboard.increment()
                pipe.passed = True
            elif pipe.x + pipe.width < 0: 
                pipe.reset()
    
        scoreboard.draw_score(game_surface)

        # collision with roof and floor
        if bird.y > 300 or bird.y < 0: 
            game_over = True
        # collision with pipes
        if bird.rect.collidelist([pipe.top_rect for pipe in pipes]) != -1 or bird.rect.collidelist([pipe.bottom_rect for pipe in pipes]) != -1 or bird.rect.collidelist([floor.rect1, floor.rect2]) != -1:
            game_over = True
        
        if game_over: 
            game_on = False
            game_over_screen(scoreboard)
            break
        
        #Rendering the game surface to the window
        scaled = pygame.transform.smoothscale(game_surface, screen.get_size())
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    global screen
    play_button = Button(220, 150, 200, 50, "Play")
    quit_button = Button(220, 250, 200, 50, "Quit")
    background = BackgroundObject(BACKGROUND_IMG, speed=1)
    floor = BackgroundObject(FLOOR_IMG, speed=3, y=300)
    while True:
        background.update()
        floor.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if screen.get_flags() & pygame.FULLSCREEN:
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                scale_x = WINDOW_WIDTH / screen.get_width()
                scale_y = WINDOW_HEIGHT / screen.get_height()
                scaled_pos = (event.pos[0] * scale_x, event.pos[1] * scale_y)
                if play_button.rect.collidepoint(scaled_pos):
                    new_game()
                elif quit_button.rect.collidepoint(scaled_pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                new_game()
        
        game_surface.fill((255, 255, 255))
        background.draw(game_surface)
        floor.draw(game_surface)
        draw_text(game_surface, "Flappy Bird", 64, (255, 255, 255), 320, 80, None)
        play_button.draw(game_surface)
        quit_button.draw(game_surface)

        scaled = pygame.transform.smoothscale(game_surface, screen.get_size())
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(scoreboard):
    global screen
    while True:
        game_surface.fill((0, 0, 0))
        scoreboard.draw_game_over(game_surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        scaled = pygame.transform.smoothscale(game_surface, screen.get_size())
        screen.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

while running:
    main_menu()
    
 
pygame.quit()
sys.exit()

