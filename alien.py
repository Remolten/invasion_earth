import pygame
from pygame.locals import *

import random

def groupcollidemodded(groupa, groupb):
    for sprite in groupa.sprites():
        for s in groupb.sprites():
            if sprite.rect.colliderect(s.rect):
                s.kill()
                sprite.dead()

class Alien(pygame.sprite.DirtySprite):
    def __init__(self, screen_size_x, screen_size_y):
        pygame.sprite.DirtySprite.__init__(self)
        self.types = 'Blue', 'Green', 'Red', 'Yellow'
        self.type = random.choice(self.types)
        self.image = pygame.image.load('ufo' + self.type + '.png').convert()
        self.rect = pygame.Rect(random.randint(0, screen_size_x - 99), 0, 91, 91)
        self.screen_size_y = screen_size_y
        if self.type == 'Red':
            self.speed = 6
        else:
            self.speed = 4
        if self.type == 'Blue':
            #Nerfs in progress
            self.health = 6
        else:
            self.health = 1
        if self.type == 'Yellow':
            self.shooter = True
        else:
            self.shooter = False
        #self.rotation = 1
        self.dirty = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.y + 91 >= self.screen_size_y:
            self.kill()

        if self.shooter:
            pass
        '''if self.rotation == 1:
            pygame.transform.rotate(self.image, 30)
            self.rotation += 1
        if self.rotation == 6:
            pygame.transform.rotate(self.image, -30)
            self.rotation = 0'''

    def dead(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
