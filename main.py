# 
# Copyright (C) Tue Jul 19 2016 Remington Thurber 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame.locals import *

import sys, os

from ecsgame import *

class Game(ecsGame):
    def __init__(self):
        self.ssx = 800
        self.ssy = 600
        self.gameover = False
        pygame.init()
        self.screen = pygame.display.set_mode((self.ssx, self.ssy))
        self.screenRect = self.screen.get_rect()
        pygame.display.set_caption('Invasion Earth')
        self.clock = pygame.time.Clock()
        
        # Below should be implemented but is not atm
        self.dt = 0
        
        self.font = pygame.font.SysFont("monospace", 60)

        # TODO this probably needs to be changed but it will suffice for now
        # Make a system/function for the loading and downscaling
        self.bg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'Backgrounds', 'Parallax100.png')).convert()
        self.plrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'playerShip3_green.png')).convert_alpha()
        self.alimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'ufoYellow.png')).convert_alpha()
        self.lsrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Lasers', 'laserBlue01.png')).convert_alpha()
        self.jet1 = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Effects', 'fire01.png')).convert_alpha()
        self.jet4 = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Effects', 'fire04.png')).convert_alpha()
        self.jet5 = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Effects', 'fire05.png')).convert_alpha()
        
        self.jetimgs = [self.jet1, self.jet4, self.jet5]

        # Scale down by factor of 3
        downscale = 3
        self.plrimg = pygame.transform.scale(self.plrimg, (self.plrimg.get_width() / downscale, self.plrimg.get_height() / downscale))
        self.alimg = pygame.transform.scale(self.alimg, (self.alimg.get_width() / downscale, self.alimg.get_height() / downscale))
        self.lsrimg = pygame.transform.scale(self.lsrimg, (self.lsrimg.get_width() / downscale, self.lsrimg.get_height() / downscale))
        self.jet1 = pygame.transform.scale(self.jet1, (self.jet1.get_width() / 2, self.jet1.get_height() / 2))
        self.jet4 = pygame.transform.scale(self.jet4, (self.jet4.get_width() / 2, self.jet4.get_height() / 2))
        self.jet5 = pygame.transform.scale(self.jet5, (self.jet5.get_width() / 2, self.jet5.get_height() / 2))

        # TODO these must be changed to conform to the new game object
        self.entityGroupSystem = EntityGroupSystem()
        self.eventSystem = EventSystem()
        self.movementSystem = MovementSystem()
        self.fireSystem = FireSystem()
        self.drawSystem = DrawSystem()
        self.alienGeneratorSystem = AlienGeneratorSystem()
        self.jetAnimationSystem = JetAnimationSystem()

    def start(self):
        # TODO fix all of these with the new api
        self.entities = []
        self.plr = self.Entity('player', DirtySprite(self.plrimg, self.plrimg.get_rect(x = self.ssx / 2 - self.plrimg.get_width() / 2, y = self.ssy / 2 - self.plrimg.get_height() / 2)), Speed(6, 6, 0.08), PlayerControl(), Fire(), Movement(), Events())
        self.spriteGroup = pygame.sprite.OrderedUpdates(self.plr.DirtySprite)
        self.entities, self.spriteGroup = self.jetAnimationSystem.create(self.entities, self.plr.id, self.spriteGroup, self.jetimgs)
        self.entities.append(self.plr)
        self.entitiesDict = self.entityGroupSystem.isort(self.entities)
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
            self.jetAnimationSystem.update(self.entities)
            rlst = self.drawSystem.draw(self.screen, self.screenRect, self.bg, self.spriteGroup)

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
