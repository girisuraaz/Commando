import pygame
import math
from random import randint

from bullet import Bullet


class Cannon(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super(Cannon, self).__init__()
        self.cannon_image = pygame.image.load("sprites/cannon.png")
        self.image = self.cannon_image
        self.rect = self.image.get_rect(x=start_x, y=start_y)
        self.timer = randint(0, 100)
        self.angle = 0

    def update(self, soldier, bullet_group, keys):
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5
        elif keys[pygame.K_LEFT]:
            self.rect.x += 5
        angle = self.angle - math.atan2(soldier.rect.y - self.rect.y, soldier.rect.x - self.rect.x)
        self.image = pygame.transform.rotate(self.cannon_image, math.degrees(angle) + 180)
        if self.timer == 0:
            bullet = Bullet(self.rect.x, self.rect.y + 25, soldier.rect.centerx, soldier.rect.centery)
            bullet_group.add(bullet)
        self.timer -= 1
        if self.timer < 0:
            self.timer = randint(50, 150)

