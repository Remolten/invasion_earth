import pygame
from pygame.locals import *

class EventSystem():
    def __init__(self):
        pass

    def update(self, entities, event):
        for id, entity in entities.iteritems():
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

                    if event.key == K_UP or event.key == ord('w'):
                        entity.cs['PlayerControl'].up = False
                    if event.key == K_DOWN or event.key == ord('s'):
                        entity.cs['PlayerControl'].dwn = False
                    if event.key == K_LEFT or event.key == ord('a'):
                        entity.cs['PlayerControl'].lft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        entity.cs['PlayerControl'].rgt = False

class MovementSystem():
    def __init__(self):
        pass

    def update(self, entities):
        for id, entity in entities.iteritems():
            if entity.cs['DirtySprite'] != None and entity.cs['Speed'] != None:
                if entity.cs['PlayerControl'] != None:
                    #FIXME Does not detect the up down etc. ????
                    if entity.cs['PlayerControl'].up:
                        entity.cs['DirtySprite'].rect -= entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    elif entity.cs['PlayerControl'].dwn:
                        entity.cs['DirtySprite'].rect += entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    if entity.cs['PlayerControl'].lft:
                        entity.cs['DirtySprite'].rect -= entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    elif entity.cs['PlayerControl'].rgt:
                        entity.cs['DirtySprite'].rect += entity.cs['Speed'].spd
                        entity.cs['DirtySprite'].dirty = 1
                    if not entity.cs['PlayerControl'].up and not entity.cs['PlayerControl'].dwn and not entity.cs['PlayerControl'].lft and not entity.cs['PlayerControl'].rgt:
                        entity.cs['DirtySprite'].dirty = 0

class DrawSystem():
    def __init__(self):
        self.rlst = []

    def draw(self, screen, *args):
        self.rlst = []
        for group in args:
            rcts = group.draw(screen)
            try:
                self.rlst.extend(*rcts)
            except:
                pass

class EntityGroupSystem():
    def __init__(self):
        pass
