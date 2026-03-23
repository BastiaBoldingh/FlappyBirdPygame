import pygame

class BackgroundObject: 
    def __init__(self, img, speed, y=0):
        self.image = img
        self.speed = speed
        self.x1 = 0
        self.x2 = self.image.get_width()
        self.y = y

    def update(self, speed_multiplier=1.0):
        self.x1 -= self.speed * speed_multiplier
        self.x2 -= self.speed * speed_multiplier
        if self.x1 <= -self.image.get_width():
            self.x1 = self.image.get_width() + self.x2
        if self.x2 <= -self.image.get_width():
            self.x2 = self.image.get_width() + self.x1
    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))

