import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame.locals import *

import sys, os, random

from entity import *
from components import *
from systems import *

class Game:
    def __init__(self):
        self.ssx = 1000
        self.ssy = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.ssx, self.ssy))
        pygame.display.set_caption('Invasion Earth')
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'Backgrounds', 'purple.png')).convert()
        self.plrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'playerShip3_green.png')).convert_alpha()

        self.eventSystem = EventSystem()
        self.movementSystem = MovementSystem(self.screen.get_rect())
        self.drawSystem = DrawSystem()

    def start(self):
        self.entities = []
        self.plr = Entity('plr', DirtySprite(self.plrimg, self.plrimg.get_rect(x = self.ssx / 2 - self.plrimg.get_width() / 2, y = self.ssy / 2 - self.plrimg.get_height() / 2)), Speed(5, 6, 0.06), PlayerControl(), Fire())
        self.entities.append(self.plr)
        self.plrgrp = pygame.sprite.OrderedUpdates(self.plr.DirtySprite)
        #aliens = OrderedUpdatesModded()
        #powerups = OrderedUpdatesModded()

    def run(self):
        self.start()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                self.eventSystem.update(self.entities, event)

                '''if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pass
                    if event.key == K_UP or event.key == ord('w'):
                        self.self.plr.move_up = True
                        self.plr.move_down = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        self.plr.move_down = True
                        self.plr.move_up = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        self.plr.move_left = True
                        self.plr.move_right = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        self.plr.move_right = True
                        self.plr.move_left = False
                    if event.key == K_SPACE:
                        self.plr.shooting = True
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        self.plr.flash = True

                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        if fullscreen:
                            pygame.display.set_mode((screen_size_x, screen_size_y))
                            fullscreen = False
                        else:
                            pygame.display.set_mode((screen_size_x, screen_size_y),
                                                    FULLSCREEN)
                            fullscreen = True
                    if event.key == K_UP or event.key == ord('w'):
                        self.plr.move_up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        self.plr.move_down = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        self.plr.move_left = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        self.plr.move_right = False
                    if event.key == K_SPACE:
                        self.plr.shooting = False
                    if event.key == K_LSHIFT or event.key == K_RSHIFT:
                        self.plr.flash = False

                if event.type == MOUSEBUTTONDOWN:
                    #Left = 1, Scroll Wheel = 2 Right = 3 Close = 6 Far = 7
                    #Only triggers on left mouse clicks
                    if event.button == 1:
                        self.plr.shooting = True

                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.plr.shooting = False'''

            #Maybe move this code
            #TODO Change this to spritecollide group function
            '''for alien in aliens.sprites():
                if self.plr.rect.colliderect(alien):
                    alien.kill()
                    if self.plr.active_powerup != 'shield':
                        self.plr.damage()
                    else:
                        self.plr.active_powerup = None

            #Do something when self.plr hits a powerup
            for powerup in powerups.sprites():
                if self.plr.rect.colliderect(powerup):
                    self.plr.active_powerup = powerup.type
                    powerup.kill()

            #Just a temporary test
            if self.plr.dead:
                print('Game Over')
                pygame.quit()
                sys.exit()

            if random.randint(0, 120) == 11:
                alien = Alien(window_rect)
                aliens.add(alien)

            if self.plr.active_powerup == 'bolt':
                aliens.empty()
                self.plr.active_powerup = None

            if random.randint(0, 240) == 11 and self.plr.active_powerup == None:
                powerup = Powerup(window_rect)
                powerups.add(powerup)

            groupcollidemodded(aliens, self.plr.bolts_group)
            if self.plr.active_powerup != 'star':
                aliens.update()'''

            '''aliens.draw(window)
            powerups.update()
            powerups.draw(window)
            self.plr.new_bolts()
            self.plr.bolts_group.update()
            self.plr.bolts_group.draw(window)'''
            #self.plr.update()
            #self.plrgrp.draw(window)
            #TODO create the groups
            self.movementSystem.update(self.entities)
            self.drawSystem.draw(self.screen, self.bg, self.plrgrp)
            pygame.display.update(self.drawSystem.rlst)
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
