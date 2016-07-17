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
        self.gameover = False
        pygame.init()
        self.screen = pygame.display.set_mode((self.ssx, self.ssy))
        self.screenRect = self.screen.get_rect()
        pygame.display.set_caption('Invasion Earth')
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.font = pygame.font.SysFont("monospace", 60)

        # TODO this probably needs to be changed but it will suffice for now
        self.bg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'Backgrounds', 'purple.png')).convert()
        self.plrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'playerShip3_green.png')).convert_alpha()
        self.alimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'ufoYellow.png')).convert_alpha()
        self.lsrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Lasers', 'laserBlue01.png')).convert_alpha()

        # Scale down by factor of 3
        downscale = 3
        self.plrimg = pygame.transform.scale(self.plrimg, (self.plrimg.get_width() / downscale, self.plrimg.get_height() / downscale))
        self.alimg = pygame.transform.scale(self.alimg, (self.alimg.get_width() / downscale, self.alimg.get_height() / downscale))
        self.lsrimg = pygame.transform.scale(self.lsrimg, (self.lsrimg.get_width() / downscale, self.lsrimg.get_height() / downscale))

        self.entityGroupSystem = EntityGroupSystem()
        self.eventSystem = EventSystem()
        self.movementSystem = MovementSystem()
        self.fireSystem = FireSystem()
        self.drawSystem = DrawSystem()
        self.alienGeneratorSystem = AlienGeneratorSystem()

    def start(self):
        self.entities = []
        self.plr = Entity('plr', DirtySprite(self.plrimg, self.plrimg.get_rect(x = self.ssx / 2 - self.plrimg.get_width() / 2, y = self.ssy / 2 - self.plrimg.get_height() / 2)), Speed(6, 6, 0.08), PlayerControl(), Fire(), Movement(), Events())
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
                    #pygame.quit() #seg faults for some reason
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        #pygame.quit()
                        sys.exit()

                #call the egs outside of loop first to optimize
                self.eventSystem.update(event, self.entityGroupSystem.get(self.entitiesDict, 'Events'))

            self.entities, self.spriteGroup = self.alienGeneratorSystem.gen(self.entities, self.alimg, self.screenRect, self.spriteGroup)
            self.entitiesDict = self.entityGroupSystem.sort(self.entitiesDict, self.entities)
            self.movementSystem.update(self.screenRect, self.entityGroupSystem.get(self.entitiesDict, 'Movement'), self.plr)
            self.fireSystem.update(self.entities, self.spriteGroup, self.lsrimg, self.plr)
            self.movementSystem.move(self.screenRect, self.entityGroupSystem.get(self.entitiesDict, 'Movement'))
            rlst = self.drawSystem.draw(self.screen, self.bg, self.spriteGroup)

            for alien in self.entityGroupSystem.get(self.entitiesDict, 'Alien'):
                if self.plr.DirtySprite.rect.colliderect(alien.DirtySprite.rect):
                    self.entitiesDict, self.entities, self.spriteGroup = self.entityGroupSystem.destroy(self.entitiesDict, self.entities, self.spriteGroup, alien)
                    self.gameover = True
                    ct = 0
                #quick hack to check that alien is not already destroyed, inefficient change later
                for laser in self.entityGroupSystem.get(self.entitiesDict, 'Laser'):
                    if laser.DirtySprite.rect.colliderect(alien.DirtySprite.rect) and alien in self.entities:
                        self.entitiesDict, self.entities, self.spriteGroup = self.entityGroupSystem.destroy(self.entitiesDict, self.entities, self.spriteGroup, alien, laser)
            if self.gameover:
                ct += 1
                self.screen.blit(self.font.render("wATch out", 1, (255,255,0)), (self.ssx / 8, self.ssy / 3))
                if ct == 120:
                    ct = 0
                    self.gameover = False

            pygame.display.update(rlst)
            self.dt = self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
