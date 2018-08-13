import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y):
        super(Bullet, self).__init__()
        self.image = pygame.image.load("sprites/bullet.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(x=start_x, y=start_y)
        self.timer = 0.0
        self.angle = 0
        self.target_x = end_x
        self.target_y = end_y
        angle = self.angle - math.atan2(end_y - start_y, end_x - start_x)
        self.speed_x = 5 * math.cos(angle)
        self.speed_y = 5 * math.sin(angle)

    def update(self, keys, bullet_group):
        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5
        elif keys[pygame.K_LEFT]:
            self.rect.x += 5
        self.rect.x += self.speed_x
        self.rect.y -= self.speed_y
        if self.rect.y > 600 or self.rect.y<50:
            self.remove(bullet_group)
            self.kill()



