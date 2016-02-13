import pygame
from pygame.locals import *

import math

# Utility function which when used via yield will pause for x frames
def wait(frames):
    ct = 0
    while ct <= frames:
        ct += 1
        yield frames - ct

class EventSystem(object):
    def __init__(self):
        pass

    def update(self, entities, event):
        for entity in entities:
            if entity.has('PlayerControl', 'Fire'):
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

class MovementSystem(object):
    def __init__(self):
        pass

    def update(self, screenrect, entities):
        for entity in entities:
            if entity.has('DirtySprite', 'Speed'):
                if entity.has('PlayerControl'):
                    if entity.PlayerControl.up:
                        entity.DirtySprite.dx += entity.Speed.maxspd * math.cos(math.radians(entity.DirtySprite.angle + 90)) * entity.Speed.thrust
                        entity.DirtySprite.dy += entity.Speed.maxspd * math.sin(math.radians(entity.DirtySprite.angle - 90)) * entity.Speed.thrust
                        entity.DirtySprite.dirty = 1
                    elif entity.PlayerControl.dwn:
                        pass # Not needed unless we add virtual brakes
                    if entity.PlayerControl.lft:
                        entity.DirtySprite.angle += entity.Speed.rotspd
                        entity.DirtySprite.image = pygame.transform.rotate(entity.DirtySprite.ogimage, entity.DirtySprite.angle)
                        entity.DirtySprite.rect = entity.DirtySprite.image.get_rect(center=entity.DirtySprite.rect.center)
                        entity.DirtySprite.dirty = 1
                    elif entity.PlayerControl.rgt:
                        entity.DirtySprite.angle -= entity.Speed.rotspd
                        entity.DirtySprite.image = pygame.transform.rotate(entity.DirtySprite.ogimage, entity.DirtySprite.angle)
                        entity.DirtySprite.rect = entity.DirtySprite.image.get_rect(center=entity.DirtySprite.rect.center)
                        entity.DirtySprite.dirty = 1
                    elif not entity.PlayerControl.up: #and not entity.PlayerControl.dwn:
                        entity.DirtySprite.dirty = 0

                    # Change sprite location based on momentum
                    entity.DirtySprite.dx = entity.Speed.maxspd if entity.DirtySprite.dx > entity.Speed.maxspd else -entity.Speed.maxspd if entity.DirtySprite.dx < -entity.Speed.maxspd else entity.DirtySprite.dx
                    entity.DirtySprite.dy = entity.Speed.maxspd if entity.DirtySprite.dy > entity.Speed.maxspd else -entity.Speed.maxspd if entity.DirtySprite.dy < -entity.Speed.maxspd else entity.DirtySprite.dy
                    entity.DirtySprite.rect.x += entity.DirtySprite.dx
                    entity.DirtySprite.rect.y += entity.DirtySprite.dy

                    # Keep sprite inside the screen
                    entity.DirtySprite.rect.clamp_ip(screenrect)

class FireSystem(object):
    def __init__(self):
        pass

    def update(self, entities):
        for entity in entities:
            if entity.has('Fire'):
                if entity.Fire.fire and not entity.Fire.over:
                    entity.Fire.over = True
                    #Shoot lasers
                elif entity.Fire.over:
                    entity.Fire.overt += 1

                if entity.Fire.overt == entity.Fire.overtm:
                    entity.Fire.overt = 0
                    entity.Fire.over = False

# This must be revamped to take entity lists, not sprite groups
class DrawSystem(object):
    def __init__(self):
        pass

    def draw(self, screen, bg, *spritegroups):
        screen.fill((0, 0, 0))
        rlst = []
        for spritegroup in spritegroups:
            #group.clear(screen, bg) Needs to be the size of the screen
            rcts = spritegroup.draw(screen)
            #We are dealing with a LayeredDirty group
            #FIXME LayeredDirty groups are broken???
            if rcts != None:
                for rct in rcts:
                    rlst.append(rct)
            #We are dealing with a GroupSingle
            else:
                rlst.append(spritegroup.sprite.rect)
        return rlst

# TODO manage pygame draw groups?
class EntityGroupSystem(object):
    def __init__(self):
        pass

    def isort(self, entities):
        entitydict = {}
        return self.sort(entitydict, entities)

    def sort(self, entitydict, entities):
        for entity in entities:
            for component in entity.cs: # inefficient but functional
                entitydict[component] = [] if component not in entitydict.keys() else entitydict[component]
                entitydict[component].append(entity)
        return entitydict

    def ret(self, entitydict, *types):
        _return = []
        for type in types:
            if type in entitydict.keys():
                _return.append(entitydict[type])
        return _return
