import pygame
from pygame.locals import *

# Utility function which when used via yield will pause for x frames
def wait(frames):
    ct = 0
    while ct <= frames:
        ct += 1
        yield frames - ct

class EventSystem():
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

class MovementSystem():
    def __init__(self):
        pass

    def update(self, entities):
        for entity in entities:
            if entity.has('DirtySprite', 'Speed'):
                if entity.has('PlayerControl'):
                    if entity.PlayerControl.up:
                        entity.DirtySprite.rect.y -= entity.Speed.spd
                        entity.DirtySprite.dirty = 1
                    elif entity.PlayerControl.dwn:
                        entity.DirtySprite.rect.y += entity.Speed.spd
                        entity.DirtySprite.dirty = 1
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
                    elif not entity.PlayerControl.up and not entity.PlayerControl.dwn:
                        entity.DirtySprite.dirty = 0

class FireSystem():
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

class DrawSystem():
    def __init__(self):
        self.rlst = []

    def draw(self, screen, bg, *spritegroups):
        screen.fill((0, 0, 0))
        self.rlst = []
        for spritegroup in spritegroups:
            #group.clear(screen, bg) Needs to be the size of the screen
            rcts = spritegroup.draw(screen)
            #We are dealing with a LayeredDirty group
            #FIXME LayeredDirty groups are broken???
            if rcts != None:
                for rct in rcts:
                    self.rlst.append(rct)
            #We are dealing with a GroupSingle
            else:
                self.rlst.append(spritegroup.sprite.rect)

# Hopefully this will eventually presort entities into relevant groups
class EntityGroupSystem():
    def __init__(self):
        pass
