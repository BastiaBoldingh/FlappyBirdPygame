import pygame
import sys
from entities import Bird, Pipe, ScoreBoard
from button import Button
from background import BackgroundObject
import time
import os


pygame.init()

screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60

BACKGROUND_IMG = pygame.image.load(os.path.join('assets', 'images', 'flappy_bird_background.png')).convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (640, 360))
FLOOR_IMG = pygame.image.load(os.path.join('assets', 'images', 'flappy_bird_floor.png')).convert()



running = True

def draw_text(screen, text, size, color, x, y, font):
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect) 

def new_game(): 
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.flap()
        #Drawing background            
        screen.fill((255, 255, 255))
        background.draw(screen)
        floor.draw(screen)



        #Updating and drawing entities
        bird.update()
        bird.draw(screen)


        for pipe in pipes:
            pipe.update(speed_multiplier=speed_multiplier)
            pipe.draw(screen)
            if pipe.x < 100 and not pipe.passed: 
                scoreboard.increment()
                pipe.passed = True
            elif pipe.x + pipe.width < 0: 
                pipe.reset()
    
        scoreboard.draw_score(screen)

        #collision with roof and floor
        if bird.y > 360 or bird.y < 0: 
            game_over = True
        #collision with pipes
        if bird.rect.collidelist([pipe.top_rect for pipe in pipes]) != -1 or bird.rect.collidelist([pipe.bottom_rect for pipe in pipes]) != -1:
            game_over = True
        
        if game_over: 
            game_on = False
            game_over_screen(scoreboard)
            break
        
        pygame.display.flip()
        clock.tick(FPS)

def main_menu(): 
    play_button = Button(220, 150, 200, 50, "Play")
    quit_button = Button(220, 250, 200, 50, "Quit")
    background = BackgroundObject(BACKGROUND_IMG, speed=1)
    while True:
        background.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif play_button.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                new_game()
            elif quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        
        screen.fill((255, 255, 255))
        background.draw(screen)
        draw_text(screen, "Static Cube", 64, (209, 90, 56), 320, 80, None)
        play_button.draw(screen)
        quit_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def game_over_screen(scoreboard):
    while True:
        screen.fill((0, 0, 0))
        scoreboard.draw_game_over(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.flip()
        clock.tick(FPS)

while running:
    main_menu()
    
 
pygame.quit()
sys.exit()

