import pygame
import glob
from bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    walk_list = []
    jump_list = []
    idle_list = []

    ani_list = [walk_list, jump_list, idle_list]

    lists = {0: "walk",
             1: "jump",
             2: "idle"}

    for k, v in lists.items():
        for filename in glob.glob('sprites/enemy/' + v + '/*.png'):
            im = pygame.image.load(filename)
            im = pygame.transform.scale(im, (60, 100))
            ani_list[k].append(im)

    def __init__(self, startx, starty):
        super(Enemy, self).__init__()
        self.animation_lists = self.create_animation_lists()
        self.image_list = self.animation_lists['walking']
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(x=startx, y=starty)
        self.state_dict = self.create_state_dict()
        self.state = 'idle'
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0
        self.bullet_reload = 0

    def create_animation_lists(self):
        """Creates the different lists of images for animation"""

        animation_dict = {'walking': Enemy.walk_list,
                          'jumping': Enemy.jump_list,
                          'idle': Enemy.idle_list, }
        return animation_dict

    def create_state_dict(self):
        """Creates a dictionary of a Digimon's behavior states"""
        state_dict = {'walking': self.walking,
                      'jumping': self.jumping,
                      'idle': self.resting}
        return state_dict

    def walking(self):
        self.image_list = self.animation_lists['walking']
        self.image = self.animation()

    def jumping(self):
        """Called when Digimon is in a jumping state"""
        self.image_list = self.animation_lists['jumping']
        self.image = self.animation()

    def resting(self):
        self.image_list = self.animation_lists['idle']
        self.image = self.animation()

    def animation(self):
        """Animates the Digimon"""
        if (self.current_time - self.timer) > 50:
            if self.image_index < (len(self.image_list) - 1):
                self.image_index += 1
            else:
                self.image_index = 0
            self.timer = self.current_time

        return self.image_list[self.image_index]

    def update(self, current_time, soldier, enemy_group, bullet_group, keys):
        if self.bullet_reload <= 0:
            bullet = Bullet(self.rect.x, self.rect.y, soldier.rect.x, soldier.rect.y)
            bullet_group.add(bullet)
            self.bullet_reload = 100
        self.bullet_reload -= 1

        self.current_time = current_time
        state_function = self.state_dict[self.state]
        self.handle_input(keys)
        state_function()

    def handle_input(self, keys):
        """Handle's user input"""

        if keys[pygame.K_RIGHT]:
            self.rect.x -= 5
        elif keys[pygame.K_LEFT]:
            self.rect.x += 5

        if abs(self.rect.x - 600) > abs(self.rect.x - 200):
            if self.rect.x > 200:
                self.rect.x -= 6
                if self.rect.x < 200:
                    self.rect.x = 200
            else:
                self.rect.x += 6
                if self.rect.x > 200:
                    self.rect.x = 200
        else:
            if self.rect.x > 600:
                self.rect.x -= 6
                if self.rect.x < 600:
                    self.rect.x = 600
            else:
                self.rect.x += 6
                if self.rect.x > 600:
                    self.rect.x = 600
        # else:
        #     self.state = 'idle'
