import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y):
        super(Bullet, self).__init__()
        self.image = pygame.image.load("sprites/cannon.png")
        self.rect = self.image.get_rect(x=start_x, y=start_y)
        self.timer = 0.0
        self.angle = 0
        self.target_x = end_x
        self.target_y = end_y
        angle = self.angle - math.atan2(end_y - start_y, end_x - start_x)
        self.speed_x = 5 * math.cos(angle)
        self.speed_y = 5 * math.sin(angle)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
