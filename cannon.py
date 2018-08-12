import pygame


class Cannon(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y):
        super(Cannon, self).__init__()
        self.image = pygame.image.load("sprites/cannon.png")
        self.rect = self.image.get_rect(x=start_x, y=start_y)
        self.timer = 0.0

    def update(self, current_time, keys):
        self.rect.x += 1
