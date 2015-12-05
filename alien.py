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
    def __init__(self, window_rect):
        pygame.sprite.DirtySprite.__init__(self)
        self.types = 'Blue', 'Green', 'Red', 'Yellow'
        self.type = random.choice(self.types)
        self.image = pygame.image.load('ufo' + self.type + '.png').convert_alpha()
        self.rect = pygame.Rect(random.randint(0, window_rect.w - 99), 0, 91, 91)
        self.screen_size_y = window_rect.h
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
        #self.rotation = 0
        self.dirty = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.y + 91 >= self.screen_size_y:
            self.kill()

        if self.shooter:
            pass
            
        '''if self.rotation == 0:
            self.image = pygame.transform.rotate(self.image, 30)
            self.rotation += 1
        elif self.rotation == 30:
            self.image = pygame.transform.rotate(self.image, -30)
        elif self.rotation == 60:
            self.rotation = 0
        else:
            self.rotation += 1'''
            
        

    def dead(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
