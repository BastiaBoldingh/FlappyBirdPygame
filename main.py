import pygame
import sys
from entities import Bird, Pipe, ScoreBoard
import time

pygame.init()

screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60


running = True



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
            screen.fill((0, 0, 0))
            scoreboard.draw_game_over(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

        


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                new_game()
    

pygame.quit()
sys.exit()

