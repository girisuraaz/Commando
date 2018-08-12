import pygame
import math

from bullet import Bullet


class Cannon(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super(Cannon, self).__init__()
        self.image = pygame.image.load("sprites/cannon.png")
        self.rect = self.image.get_rect(x=start_x, y=start_y)
        self.timer = 0
        self.angle = 0

    def update(self, soldier, bullet_group):
        if self.timer == 0:
            bullet = Bullet(self.rect.x, self.rect.y, soldier.rect.x, soldier.rect.y)
            bullet_group.add(bullet)
        self.timer += 1
        if self.timer == 100:
            self.timer = 0

