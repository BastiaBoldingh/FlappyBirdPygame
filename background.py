import pygame

class BackgroundObject: 
    def __init__(self, img, speed, y=0):
        self.image = img
        self.speed = speed
        self.rect1 = self.image.get_rect(topleft=(0, y))
        self.rect2 = self.image.get_rect(topleft=(self.image.get_width(), y))

    def update(self, speed_multiplier=1.0):
        self.rect1.x -= self.speed * speed_multiplier
        self.rect2.x -= self.speed * speed_multiplier
        if self.rect1.x <= -self.image.get_width():
            self.rect1.x = self.rect2.x + self.image.get_width()
        if self.rect2.x <= -self.image.get_width():
            self.rect2.x = self.rect1.x + self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, self.rect1)
        screen.blit(self.image, self.rect2)

