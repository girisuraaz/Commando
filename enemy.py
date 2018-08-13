import pygame
import math
import glob
from random import randint


from bullet import Bullet


class Enemy(pygame.sprite.Sprite):
    """Sprite player controls"""
    def __init__(self, startx, starty):
        super(Enemy, self).__init__()
        self.animation_lists = self.create_animation_lists()
        self.image_list = self.animation_lists['hunting']
        self.image_index = 0
        self.image = self.image_list[self.image_index]
        self.rect = self.image.get_rect(x=startx, y=starty)
        self.state_dict = self.create_state_dict()
        self.state = 'shooting'
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0
        self.bullet_reload = 0




    def create_list_from_images(self, location):
        # LOADING IMAGES
        image_list = []
        for filename in glob.glob('sprites/' + 'enemy/' + location + '/*.png'):
            im = pygame.image.load(filename)
            image_list.append(im)
        return image_list

    def create_animation_lists(self):
        """Creates the different lists of images for animation"""
        walk_list = self.create_list_from_images("walk")
        shoot_list = self.create_list_from_images("shoot")

        animation_dict = {'walking': walk_list,
                          'shooting': shoot_list,}
        return animation_dict

    def create_state_dict(self):
        """Creates a dictionary of a Digimon's behavior states"""
        state_dict = {'walking': self.walking,
                      'shooting': self.shoot,}
        return state_dict


    def walking(self):
        self.image_list = self.animation_lists['walking']
        self.image = self.animation()


    def shooting(self):
        self.image_list = self.animation_lists['shooting']
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

