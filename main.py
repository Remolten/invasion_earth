import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame.locals import *

import sys, os, random

from entity import *
from components import *
from systems import *

class Game(object):
    def __init__(self):
        #self.ssx = 1280
        #self.ssy = 690
        self.ssx = 800
        self.ssy = 600
        pygame.init()
        self.screen = pygame.display.set_mode((self.ssx, self.ssy))
        self.screenRect = self.screen.get_rect()
        pygame.display.set_caption('Invasion Earth')
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'Backgrounds', 'purple.png')).convert()
        self.plrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'playerShip3_green.png')).convert_alpha()
        self.alimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'ufoYellow.png')).convert_alpha()

        # Scale down by factor of 3
        downscale = 3
        self.plrimg = pygame.transform.scale(self.plrimg, (self.plrimg.get_width() / downscale, self.plrimg.get_height() / downscale))
        self.alimg = pygame.transform.scale(self.alimg, (self.alimg.get_width() / downscale, self.alimg.get_height() / downscale))

        self.entityGroupSystem = EntityGroupSystem()
        self.eventSystem = EventSystem()
        self.movementSystem = MovementSystem()
        self.drawSystem = DrawSystem()
        self.alienGeneratorSystem = AlienGeneratorSystem()

    def start(self):
        self.entities = []
        self.plr = Entity('plr', DirtySprite(self.plrimg, self.plrimg.get_rect(x = self.ssx / 2 - self.plrimg.get_width() / 2, y = self.ssy / 2 - self.plrimg.get_height() / 2)), Speed(3, 6, 0.06), PlayerControl(), Fire(), Movement(), Events())
        self.entities.append(self.plr)
        self.entitiesDict = self.entityGroupSystem.isort(self.entities)
        self.spriteGroup = pygame.sprite.OrderedUpdates(self.plr.DirtySprite)
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

                #call the egs outside of loop first to optimize
                self.eventSystem.update(event, self.entityGroupSystem.get(self.entitiesDict, 'Events'))

            self.entities, self.spriteGroup = self.alienGeneratorSystem.gen(self.entities, self.alimg, self.ssx, self.ssy, self.spriteGroup)
            self.entitiesDict = self.entityGroupSystem.sort(self.entitiesDict, self.entities)
            self.movementSystem.update(self.screenRect, self.entityGroupSystem.get(self.entitiesDict, 'Movement'))
            rlst = self.drawSystem.draw(self.screen, self.bg, self.spriteGroup)
            pygame.display.update(rlst)
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
