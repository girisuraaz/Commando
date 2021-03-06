import sys, os
import pygame
from soldier import Soldier
from cannon import Cannon
from random import randint
from enemy import Enemy

MAIN_MENU = pygame.image.load('sprites/main.jpg')
MAIN_MENU = pygame.transform.scale(MAIN_MENU, (800, 600))
MAIN_MENU_RECT = MAIN_MENU.get_rect()

BACKGROUND = pygame.image.load('flapBG.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (1600, 600))
BACKGROUND_RECT = BACKGROUND.get_rect()


class Game(object):
    """Controls entire game"""
    def __init__(self):
        self.soldier = Soldier(400, 400)
        self.health = 100
        self.screen = self.setup_pygame()
        self.font = self.setup_font()
        self.screen_rect = self.screen.get_rect()
        self.soldier_group = self.create_digimon()
        self.enemy_group = self.create_bullet()
        self.cannon_group = self.create_cannon()
        self.bullet_group = self.create_bullet()
        self.player_bullet_group = self.create_bullet()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False
        self.current_time = 0.0
        self.speed = 5
        self.mode = "main_menu"
        self.play = pygame.Rect(150, 450, 100, 50)
        self.exit = pygame.Rect(550, 450, 100, 50)


    def setup_pygame(self):
        """Initializes pygame and produces a surface to blit on"""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Commando')
        screen = pygame.display.set_mode((800, 600))

        return screen

    def setup_font(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        return myfont

    def update_text(self):
        textsurface = self.font.render('Health : ' + str(self.health), False, (0, 0, 0))
        return textsurface

    def create_digimon(self):
        sprite_group = pygame.sprite.Group()
        sprite_group.add(self.soldier)
        return sprite_group

    def create_cannon(self):
        """Creates a digimon to control"""
        sprite_group = pygame.sprite.Group()
        for i in range(0, 10):
            cannon = Cannon(randint(0, 1000) + i * 1000, 50)
            sprite_group.add(cannon)
        return sprite_group

    def create_bullet(self):
        sprite_group = pygame.sprite.Group()
        return sprite_group

    def update(self):
        """Updates entire game"""
        while not self.done:
            self.keys = self.get_user_input()
            if self.mode == "main_menu":
                self.screen.blit(MAIN_MENU, (MAIN_MENU_RECT.x, 0, 800, 600))

                pygame.draw.rect(self.screen, (255, 255, 255, 255), self.play)
                pygame.draw.rect(self.screen, (255, 255, 255, 255), self.exit)
                if self.keys[pygame.K_KP_ENTER]:
                    self.mode = "game"

            else:
                # GAME LOGIC
                self.current_time = pygame.time.get_ticks()

                if self.keys[pygame.K_RIGHT]:
                    BACKGROUND_RECT.x -= self.speed
                elif self.keys[pygame.K_LEFT]:
                    BACKGROUND_RECT.x += self.speed
                if BACKGROUND_RECT.x < -800:
                    BACKGROUND_RECT.x = 0
                elif BACKGROUND_RECT.x > 0:
                    BACKGROUND_RECT.x = -800

                for bullet in pygame.sprite.spritecollide(self.soldier, self.bullet_group, 1):
                    self.health -= 5

                for bullet in self.player_bullet_group:
                    for cannon in pygame.sprite.spritecollide(bullet, self.cannon_group, 1):
                        pass
                    for enemy in pygame.sprite.spritecollide(bullet, self.enemy_group, 1):
                        pass

                if self.health <= 0:
                    print("GAME OVER!")
                    sys.exit(0)

                # create enemy random
                if randint(0, 300) == 0:
                    if randint(0, 1) == 0:
                        self.enemy_group.add(Enemy(900, 400))
                    else:
                        self.enemy_group.add(Enemy(-100, 400))


                # FRAME UPDATES
                self.soldier_group.update(self.current_time, self.keys, self.player_bullet_group)
                self.enemy_group.update(self.current_time, self.soldier, self.enemy_group, self.bullet_group, self.keys)
                self.cannon_group.update(self.soldier, self.bullet_group, self.keys)
                self.bullet_group.update(self.keys, self.bullet_group)
                self.player_bullet_group.update(self.keys, self.player_bullet_group)
                self.screen.blit(BACKGROUND, (BACKGROUND_RECT.x, 0, 800, 600))
                self.soldier_group.draw(self.screen)
                self.enemy_group.draw(self.screen)
                self.cannon_group.draw(self.screen)
                self.bullet_group.draw(self.screen)
                self.player_bullet_group.draw(self.screen)
                self.screen.blit(self.update_text(), (0, 0))
            pygame.display.update()
            self.clock.tick(self.fps)


    def get_user_input(self):
        """Get's user events and keys pressed"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.play.collidepoint(pos):
                    self.mode = game
                elif self.exit.collidepoint(pos):
                    self.done = True

        keys = pygame.key.get_pressed()

        return keys


if __name__ == '__main__':
    game = Game()
    game.update()
    pygame.quit()
    sys.exit()

















