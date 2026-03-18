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

bird = Bird(100, 180)
pipes = [Pipe()]
scoreboard = ScoreBoard()


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                bird.flap()

    # Loss condition
    if bird.y > 360 or bird.y < 0: 
        print("Game Over!")
        time.sleep(2)
        running = False


    screen.fill((255, 255, 255))

    bird.update()
    screen.blit(bird.image, (bird.x, bird.y))

    for pipe in pipes:
        pipe.update()
        pipe.draw(screen)
    
    scoreboard.draw_score(screen)


    pygame.display.flip()
    clock.tick(FPS)

screen.fill((0, 0, 0))
scoreboard.draw_game_over(screen)

pygame.quit()
sys.exit()

