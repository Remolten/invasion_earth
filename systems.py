import pygame
from pygame.locals import *

class EventSystem():
    def __init__(self):
        pass

    def update(self, entities, event):
        for entity in entities:
            if entity.cs['PlayerControl'] != None:
                if event.type == KEYDOWN:
                    if event.key == K_UP or event.key == ord('w'):
                        entity.cs['PlayerControl'].up = True
                        entity.cs['PlayerControl'].dwn = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        entity.cs['PlayerControl'].dwn = True
                        entity.cs['PlayerControl'].up = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        entity.cs['PlayerControl'].lft = True
                        entity.cs['PlayerControl'].rgt = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        entity.cs['PlayerControl'].rgt = True
                        entity.cs['PlayerControl'].lft = False
                    if event.key == K_SPACE and entity.cs['Fire'] != None:
                        entity.cs['Fire'].fire = True
                        entity.cs['Fire'].over = True

                if event.type == KEYUP:
                    if event.key == K_UP or event.key == ord('w'):
                        entity.cs['PlayerControl'].up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        entity.cs['PlayerControl'].dwn = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        entity.cs['PlayerControl'].lft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        entity.cs['PlayerControl'].rgt = False
                    if event.key == K_SPACE and entity.cs['Fire'] != None:
                        entity.cs['Fire'].fire = False

class MovementSystem():
    def __init__(self):
        pass

    def update(self, entities):
        for entity in entities:
            if entity.cs['DirtySprite'] != None and entity.cs['Speed'] != None:
                if entity.cs['PlayerControl'] != None:
                    #FIXME Dirty is glitched up
                    if entity.cs['PlayerControl'].up:
                        entity.cs['DirtySprite'].rect.y -= entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    elif entity.cs['PlayerControl'].dwn:
                        entity.cs['DirtySprite'].rect.y += entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    if entity.cs['PlayerControl'].lft:
                        entity.cs['DirtySprite'].rect.x -= entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    elif entity.cs['PlayerControl'].rgt:
                        entity.cs['DirtySprite'].rect.x += entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    elif not entity.cs['PlayerControl'].up and not entity.cs['PlayerControl'].dwn:
                        entity.cs['DirtySprite'].dirty = 0

class FireSystem():
    def __init__(self):
        pass

    def update(self, entities):
        for entity in entities:
            if entity.cs['Fire'].fire and not entity.cs['Fire'].over:
                pass #Shoot lasers
            elif entity.cs['Fire'].over:
                entity.cs['Fire'].overt += 1

            if entity.cs['Fire'].overt == entity.cs['Fire'].overtm:
                entity.cs['Fire'].overt = 0
                entity.cs['Fire'].over = False

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
