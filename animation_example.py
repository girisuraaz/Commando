import sys, os
import pygame
import glob

BACKGROUND = pygame.image.load('flapBG.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (800, 600))
BACKGROUND_RECT = BACKGROUND.get_rect()

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
        self.state = 'resting'
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0

    def create_list_from_images(self, type):
        # LOADING IMAGES
        image_list = []
        for filename in glob.glob('sprites/' + type + '/*.png'):
            im = pygame.image.load(filename)
            image_list.append(im)
        return image_list

    def create_animation_lists(self):
        """Creates the different lists of images for animation"""
        walk_list = self.create_list_from_images("walk")
        jump_list = self.create_list_from_images("jump")

        animation_dict = {'walking': walk_list,
                          'jumping': jump_list}
        return animation_dict

    def create_state_dict(self):
        """Creates a dictionary of a Digimon's behavior states"""
        state_dict = {'walking': self.walking,
                      'jumping': self.jumping,
                      'resting': self.resting}
        return state_dict

    def walking(self):
        """Called when Digimon is in a walking state"""
        if self.direction == 'left':
            self.x_vel = -5
        else:
            self.x_vel = 5

        self.image_list = self.animation_lists['walking']
        self.rect.x += self.x_vel
        self.image = self.animation()


    def jumping(self):
        """Called when Digimon is in a jumping state"""
        self.image_list = self.animation_lists['jumping']
        self.rect.y += self.y_vel
        self.image = self.animation()


    def resting(self):
        """Called when Digimon is stationary"""
        pass


    def animation(self):
        """Animates the Digimon"""
        if (self.current_time - self.timer) > 50:
            if self.image_index < (len(self.image_list) - 1):
                self.image_index += 1
            else:
                self.image_index = 0
            self.timer = self.current_time

        return self.image_list[self.image_index]


    def update(self, current_time, keys):
        """Updates Digimon state"""
        self.current_time = current_time
        self.handle_input(keys)
        state_function = self.state_dict[self.state]
        state_function()


    def handle_input(self, keys):
        """Handle's user input"""
        if keys[pygame.K_UP]:
            self.state = 'jumping'
            self.direction = 'up'
        elif keys[pygame.K_RIGHT]:
            self.state = 'walking'
            self.direction = 'right'
        elif keys[pygame.K_LEFT]:
            self.state = 'walking'
            self.direction = 'left'
        elif keys[pygame.K_DOWN]:
            self.state = 'jumping'
            self.direction = 'down'
        else:
            self.state = 'resting'


class Game(object):
    """Controls entire game"""
    def __init__(self):
        self.screen = self.setup_pygame()
        self.screen_rect = self.screen.get_rect()
        self.digimon_group = self.create_digimon()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False
        self.current_time = 0.0


    def setup_pygame(self):
        """Initializes pygame and produces a surface to blit on"""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption('Digimon Game')
        screen = pygame.display.set_mode((800, 600))

        return screen


    def create_digimon(self):
        """Creates a digimon to control"""
        sprite_group = pygame.sprite.Group()
        digimon = Soldier(100, 500)
        sprite_group.add(digimon)

        return sprite_group


    def update(self):
        """Updates entire game"""
        while not self.done:
            self.current_time = pygame.time.get_ticks()
            self.keys = self.get_user_input()
            self.digimon_group.update(self.current_time, self.keys)
            self.screen.blit(BACKGROUND, BACKGROUND_RECT)
            self.digimon_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(self.fps)


    def get_user_input(self):
        """Get's user events and keys pressed"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        keys = pygame.key.get_pressed()

        return keys


if __name__ == '__main__':
    game = Game()
    game.update()
    pygame.quit()
    sys.exit()

















