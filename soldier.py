import pygame
import glob
from bullet import Bullet


class Soldier(pygame.sprite.Sprite):
    """Sprite player controls"""

    def __init__(self, startx, starty):
        super(Soldier, self).__init__()
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
        self.jump = False
        self.jump_velocity = 20
        self.jump_current_velocity = self.jump_velocity

    def create_list_from_images(self, location):
        # LOADING IMAGES
        image_list = []
        for filename in glob.glob('sprites/' + location + '/*.png'):
            im = pygame.image.load(filename)
            image_list.append(im)
        return image_list

    def create_animation_lists(self):
        """Creates the different lists of images for animation"""
        walk_list = self.create_list_from_images("walk")
        jump_list = self.create_list_from_images("jump")
        idle_list = self.create_list_from_images("idle")

        animation_dict = {'walking': walk_list,
                          'jumping': jump_list,
                          'idle': idle_list, }
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

    def update(self, current_time, keys, player_bullet_group):
        if self.rect.y > 400:
            self.jump = False
            self.jump_current_velocity = self.jump_velocity
            self.rect.y = 400
        if self.jump:
            self.rect.y -= self.jump_current_velocity
            self.jump_current_velocity -= 1

        """Updates Digimon state"""
        if pygame.mouse.get_pressed()[0]:
            if self.bullet_reload <= 0:
                bullet = Bullet(self.rect.x, self.rect.y + 25, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                player_bullet_group.add(bullet)
                self.bullet_reload = 20
        self.bullet_reload -= 1

        self.current_time = current_time
        if not self.jump:
            self.handle_input(keys)
        state_function = self.state_dict[self.state]
        state_function()

    def handle_input(self, keys):
        """Handle's user input"""
        if keys[pygame.K_UP]:
            self.jump = True
            self.state = 'jumping'
            self.direction = 'up'
        elif keys[pygame.K_RIGHT]:
            self.state = 'walking'
            self.direction = 'right'
        elif keys[pygame.K_LEFT]:
            self.state = 'walking'
            self.direction = 'left'
        else:
            self.state = 'idle'
