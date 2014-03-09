import pygame
from pygame.locals import *

#Use this module to determine slant for flash
from fractions import Fraction

class OrderedUpdatesModded(pygame.sprite.OrderedUpdates):
    def update(self, *args):
        #This makes the group's sprite's updating internalized
        for sprite in list(self.spritedict):
            sprite.update(*args)

class Bolt(pygame.sprite.DirtySprite):
    def __init__(self, x, y, image):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = pygame.Rect(x, y, 13, 37)
        self.dirty = 2

    def update(self):
        self.rect.y -= 12
        if self.rect.y <= 0:
            self.kill()
            
class Player(pygame.sprite.DirtySprite):
    def __init__(self, screen_size_x, screen_size_y):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load('player.png')
        self.bolt_image = pygame.image.load('laser.png')
        self.rect = pygame.Rect(screen_size_x / 2 - 45, screen_size_y - 75, 99, 75)
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.shooting = False
        self.overheated = False
        self.bolts_group = OrderedUpdatesModded()
        self.counter = 0
        self.health = 3
        self.flash = False
        self.flash_cd = False
        self.flash_counter = 0
        self.dead = False
        self.dirty = 0

    def update(self, screen_size_x, screen_size_y):          
        if self.move_up and self.rect.y >= 0:
            self.rect.y -= 6
            self.dirty = 1
        if self.move_down and self.rect.y + self.rect.h <= screen_size_y:
            self.rect.y += 6
            self.dirty = 1
        if self.move_left and self.rect.x >= 0:
            self.rect.x -= 6
            self.dirty = 1
        if self.move_right and self.rect.x + self.rect.w <= screen_size_x:
            self.rect.x += 6
            self.dirty = 1

        if self.flash and not self.flash_cd:
            x, y = pygame.mouse.get_pos()
            self.rect.centerx, self.rect.centery = x, y
            if x < 0:
                self.rect.x = 0
            if y < 0:
                self.rect.y = 0
            if x + self.rect.w > screen_size_x:
                self.rect.x = screen_size_x - self.rect.w
            if y + self.rect.h > screen_size_y:
                self.rect.y = screen_size_y - self.rect.h
            self.flash_cd = True
        else:
            self.flash_counter += 1
            if self.flash_counter == 120:
                self.flash_cd = False
                self.flash_counter = 0

    def new_bolts(self):
        #Clean this up?
        if self.shooting and not self.overheated:
            bolt = Bolt(self.rect.x, self.rect.y, self.bolt_image)
            bolt_2 = Bolt(self.rect.x + self.rect.w - 13, self.rect.y,
                          self.bolt_image)
            self.bolts_group.add(bolt, bolt_2)
            self.overheated = True
        else:
            self.counter += 1
            if self.counter == 8:
                self.counter = 0
                self.overheated = False

