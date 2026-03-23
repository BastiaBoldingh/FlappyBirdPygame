import pygame

class Background: 
    def __init__(self, img, speed):
        self.image = img
        self.speed = speed
        self.x1 = 0
        self.x2 = self.image.get_width()
    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 <= -self.image.get_width():
            self.x1 = self.image.get_width()
        if self.x2 <= -self.image.get_width():
            self.x2 = self.image.get_width()
    def draw(self, screen):
        screen.blit(self.image, (self.x1, 0))
        screen.blit(self.image, (self.x2, 0))