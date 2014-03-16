import pygame
from pygame.locals import *

import random

class Powerup(pygame.sprite.DirtySprite):
    def __init__(self, window_rect):
        pygame.sprite.DirtySprite.__init__(self)
        self.type = random.choice(['star', 'shield', 'bolt'])
        self.image = pygame.image.load('powerupBlue_' + self.type + '.png').convert_alpha()
        self.rect = pygame.Rect(random.randint(0, window_rect.w - 34), 33, 34, 33)
        self.dirty = 2
        self.window_rect = window_rect
        
    def update(self):
        self.rect.y += 5
        if self.rect.y + 33 >= self.window_rect.h:
            self.kill()
