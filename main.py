import pygame
import sys
from entities import Bird, Pipe, ScoreBoard
from button import Button
import time

pygame.init()

screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60


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
    counter = 0
    speed_multiplier = 1.0


    game_over = False
    game_on = True
    bird.flap()
    while game_on:
        speed_multiplier = 1 + scoreboard.score * 0.1
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.flap()
        #Drawing background            
        screen.fill((255, 255, 255))

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
                pipes.remove(pipe)
                pipes.append(Pipe())
    
        scoreboard.draw_score(screen)

        #collision with roof and floor
        if bird.y > 360 or bird.y < 0: 
            game_over = True
        #collision with pipes
        if bird.rect.collidelist([pygame.Rect(pipe.x, 0, pipe.width, pipe.top_height) for pipe in pipes]) != -1 or bird.rect.collidelist([pygame.Rect(pipe.x, 360 - pipe.bottom_height, pipe.width, pipe.bottom_height) for pipe in pipes]) != -1:
            game_over = True
        
        if game_over: 
            game_on = False
            game_over_screen(scoreboard)
            new_game()
        
        pygame.display.flip()
        clock.tick(FPS)

def main_menu(): 
    play_button = Button(220, 150, 200, 50, "Play")
    quit_button = Button(220, 250, 200, 50, "Quit")
    while True:
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
        draw_text(screen, "Flappy Bird", 64, (0, 0, 255), 320, 80, None)
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

