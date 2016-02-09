import pygame
from pygame.locals import *

class EventSystem():
    def __init__(self):
        pass

    def update(self, entities, event):
        for entity in entities:
            if entity.PlayerControl != None:
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == ord('w'):
                        entity.PlayerControl.up = True
                        entity.PlayerControl.dwn = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        entity.PlayerControl.dwn = True
                        entity.PlayerControl.up = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        entity.PlayerControl.lft = True
                        entity.PlayerControl.rgt = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        entity.PlayerControl.rgt = True
                        entity.PlayerControl.lft = False
                    if event.key == K_SPACE and entity.Fire != None:
                        entity.Fire.fire = True
                        entity.Fire.over = True

                if event.type == KEYUP:
                    if event.key == K_UP or event.key == ord('w'):
                        entity.PlayerControl.up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        entity.PlayerControl.dwn = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        entity.PlayerControl.lft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        entity.PlayerControl.rgt = False
                    if event.key == K_SPACE and entity.Fire != None:
                        entity.Fire.fire = False

class MovementSystem():
    def __init__(self):
        pass

    def update(self, entities):
        for entity in entities:
            if entity.DirtySprite != None and entity.Speed != None:
                if entity.PlayerControl != None:
                    #FIXME Dirty is glitched up
                    if entity.PlayerControl.up:
                        entity.DirtySprite.rect.y -= entity.Speed.spd
                        entity.DirtySprite.dirty = 1
                    elif entity.PlayerControl.dwn:
                        entity.DirtySprite.rect.y += entity.Speed.spd
                        entity.DirtySprite.dirty = 1
                    if entity.PlayerControl.lft:
                        entity.DirtySprite.rect.x -= entity.Speed.spd
                        entity.DirtySprite.dirty = 1
                    elif entity.PlayerControl.rgt:
                        entity.DirtySprite.rect.x += entity.Speed.spd
                        entity.DirtySprite.dirty = 1
                    elif not entity.PlayerControl.up and not entity.PlayerControl.dwn:
                        entity.DirtySprite.dirty = 0

class FireSystem():
    def __init__(self):
        pass

    def update(self, entities):
        for entity in entities:
            if entity.Fire.fire and not entity.Fire.over:
                pass #Shoot lasers
            elif entity.Fire.over:
                entity.Fire.overt += 1

            if entity.Fire.overt == entity.Fire.overtm:
                entity.Fire.overt = 0
                entity.Fire.over = False

class DrawSystem():
    def __init__(self):
        self.rlst = []

    def draw(self, screen, bg, *args):
        self.rlst = []
        for group in args:
            #group.clear(screen, bg) Needs to be the size of the screen
            rcts = group.draw(screen)
            #We are dealing with a LayeredDirty group
            #FIXME LayeredDirty groups are broken???
            if rcts != None:
                for rct in rcts:
                    self.rlst.append(rct)
            #We are dealing with a GroupSingle
            else:
                self.rlst.append(group.sprite.rect)

class EntityGroupSystem():
    def __init__(self):
        pass
