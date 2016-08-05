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

from simpyl import simpyl
from systems import *
from components import *

class Game(simpyl):
    def __init__(self):
        # Call the init method of the simpyl parent class
        super().__init__()
        
        # Screen resolution
        self.ssx = 800
        self.ssy = 600
        
        # Execute game over actions if True
        self.gameover = False
        
        # Initialize the pygame engine
        pygame.init()
        
        # Initialize the screen
        self.screen = pygame.display.set_mode((self.ssx, self.ssy))
        
        # Create a rect of the screen for convenience
        self.screenrect = self.screen.get_rect()
        
        # Set window caption text
        pygame.display.set_caption('Invasion Earth')
        
        # Create a clock for relegating frame rate
        self.clock = pygame.time.Clock()
        
        # This holds a list of events to be accessed by systems
        self.events = []
        
        # TODO Implement dt into movement to prevent framerate determining movespeed
        self.dt = 0
        
        # Load the main font, which will likely change for release
        # Maybe add a font system as well if that's needed later
        self.font = pygame.font.SysFont("monospace", 60)
        
        # Add all of the systems to the main database
        #self.addSystem(self.eventSystem, self.movementSystem, self.fireSystem, self.drawSystem, self.alienGeneratorSystem, self.collisionSystem)
        self.addSystem(EventSystem(), MovementSystem(), FireSystem(), AlienGeneratorSystem(), CollisionSystem(), HealthSystem(), AliveSystem(), GameOverSystem(), MovingBackgroundSystem(), DrawSystem())
        
        # Load all assets
        # TODO call this function with arguments for each image needed and add image + downscale args
        # This will be easily doable as soon as all assets are moved into the same location
        self.load()
        
    def load(self):
        # Load all images
        self.bg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'Backgrounds', 'spr_stars01.png')).convert()
        self.plrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'playerShip3_green.png')).convert_alpha()
        self.alimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'ufoYellow.png')).convert_alpha()
        self.lsrimg = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Lasers', 'laserBlue01.png')).convert_alpha()
        #self.jet1 = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Effects', 'fire01.png')).convert_alpha()
        #self.jet4 = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Effects', 'fire04.png')).convert_alpha()
        #self.jet5 = pygame.image.load(os.path.join(os.path.sep, os.getcwd(), 'assets', 'PNG', 'Effects', 'fire05.png')).convert_alpha()
        
        # This may not be necessary with the new refactoring
        #self.jetimgs = [self.jet1, self.jet4, self.jet5]

        # Scale down by factor of 3 for most things
        downscale = 3
        self.plrimg = pygame.transform.scale(self.plrimg, (self.plrimg.get_width() / downscale, self.plrimg.get_height() / downscale))
        self.alimg = pygame.transform.scale(self.alimg, (self.alimg.get_width() / downscale, self.alimg.get_height() / downscale))
        self.lsrimg = pygame.transform.scale(self.lsrimg, (self.lsrimg.get_width() / downscale, self.lsrimg.get_height() / downscale))
        #self.jet1 = pygame.transform.scale(self.jet1, (self.jet1.get_width() / 2, self.jet1.get_height() / 2))
        #self.jet4 = pygame.transform.scale(self.jet4, (self.jet4.get_width() / 2, self.jet4.get_height() / 2))
        #self.jet5 = pygame.transform.scale(self.jet5, (self.jet5.get_width() / 2, self.jet5.get_height() / 2))

    def start(self):
        # Hopefully should be able to call super().__init__() to reset the game
        # FUTURE relegate player creation + sprite groups to a system
        self.plr = self.Entity(DirtySprite(self.plrimg, self.plrimg.get_rect(x = self.ssx / 2 - self.plrimg.get_width() / 2, y = self.ssy / 2 - self.plrimg.get_height() / 2)), Speed(6, 6, 0.08), Player(), Health(3), Alive(), Collision(), PlayerControl(), Fire(), Movement(), Events())
        self.spriteGroup = pygame.sprite.OrderedUpdates(self.plr.DirtySprite)

    def run(self):
        self.start()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        sys.exit()

                # Add each event to the events list to be accessed by the EventSystem
                self.events.append(event)
             
            # Runs the process method of all added systems
            self.process()   
            
            #self.screen.blit(self.font.render("wATch out", 1, (255,255,0)), (self.ssx / 8, self.ssy / 3))
                    
            # Flush the events list
            self.events = []

            # Push the draw calls to the screen
            pygame.display.update(self.rlst)
            
            # Limit framerate to 60 FPS and record the delta time
            self.dt = self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
