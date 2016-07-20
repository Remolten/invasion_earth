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

import pygame
from pygame.locals import *

from entity import *
from components import *

import math, random

# Utility function which when used via yield will pause for x frames
def wait(frames):
    fr = frames
    while fr > 0:
        fr -= 1
        yield fr

class EventSystem(object):
    def __init__(self):
        pass

    def update(self, event, entities):
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

# Must separate the determination of dx dy etc. from actually editing the rect
class MovementSystem(object):
    def __init__(self):
        pass

    def update(self, screenrect, entities, player):
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
                    elif entity.DirtySprite.dx == 0 and entity.DirtySprite.dy == 0:
                        entity.DirtySprite.dirty = 0
                    elif not entity.PlayerControl.up: #and not entity.PlayerControl.dwn:
                        # Add a slight amount of friction
                        if entity.DirtySprite.dx > 0:
                            entity.DirtySprite.dx *= 0.97 #if entity.DirtySprite.dx > 0.3 else 0.9
                        elif entity.DirtySprite.dx < 0:
                            entity.DirtySprite.dx *= 0.9
                        if entity.DirtySprite.dy > 0:
                            entity.DirtySprite.dy *= 0.97 #if entity.DirtySprite.dy > 0.3 else 0.9
                        elif entity.DirtySprite.dy < 0:
                            entity.DirtySprite.dy *= 0.9
                        # you could make a case for letting the ship drift when it gets to low speeds
                        if abs(entity.DirtySprite.dx) < 0.2:
                            entity.DirtySprite.dx = 0
                        if abs(entity.DirtySprite.dy) < 0.2:
                            entity.DirtySprite.dy = 0

                if entity.has('Alien'):  
                    # Here we set the aliens to track the player
                    # All we have to do is set the angle to always face the player
                    # Get slope and convert to degrees
                    yslope = player.DirtySprite.rect.centery - entity.DirtySprite.rect.centery
                    xslope = player.DirtySprite.rect.centerx - entity.DirtySprite.rect.centerx
                    entity.DirtySprite.dx += entity.Speed.maxspd * xslope * entity.Speed.thrust
                    entity.DirtySprite.dy += entity.Speed.maxspd * yslope * entity.Speed.thrust
                    
                if entity.has('Laser'):
                    if entity.DirtySprite.rect.x <= 0 or entity.DirtySprite.rect.x >= screenrect.width - entity.DirtySprite.rect.width:
                        entity.DirtySprite.dx *= -1
                    if entity.DirtySprite.rect.y <= 0 or entity.DirtySprite.rect.y >= screenrect.height - entity.DirtySprite.rect.height:
                        entity.DirtySprite.dy *= -1
                    
                    if entity.DirtySprite.dx != 0:
                        entity.DirtySprite.angle = 90 - math.degrees(math.atan(entity.DirtySprite.dy / entity.DirtySprite.dx))
                    elif entity.DirtySprite.dy == 0:
                        entity.DirtySprite.angle = 90 if entity.DirtySprite.dx > 0 else 270
                    else:
                        entity.DirtySprite.angle = 0 if entity.DirtySprite.dy > 0 else 180
                        
                    entity.DirtySprite.image = pygame.transform.rotate(entity.DirtySprite.ogimage, entity.DirtySprite.angle)
                    entity.DirtySprite.rect = entity.DirtySprite.image.get_rect(center=entity.DirtySprite.rect.center)

                # Keeps speed under maxspd but at the same ratio
                entity.ratio = 1
                if entity.DirtySprite.dx > entity.Speed.maxspd:
                    entity.ratio = entity.Speed.maxspd / entity.DirtySprite.dx
                elif entity.DirtySprite.dx < -entity.Speed.maxspd:
                    entity.ratio = -entity.Speed.maxspd / entity.DirtySprite.dx
                if entity.DirtySprite.dy > entity.Speed.maxspd:
                    entity.ratio = entity.Speed.maxspd / entity.DirtySprite.dy
                elif entity.DirtySprite.dy < -entity.Speed.maxspd:
                    entity.ratio = -entity.Speed.maxspd / entity.DirtySprite.dy

    def move(self, screenrect, entities):
        for entity in entities:
            entity.DirtySprite.dy *= entity.ratio
            entity.DirtySprite.dx *= entity.ratio
            entity.DirtySprite.rect.x += entity.DirtySprite.dx
            entity.DirtySprite.rect.y += entity.DirtySprite.dy

            # Keep sprite inside the screen
            entity.DirtySprite.rect.clamp_ip(screenrect)

class FireSystem(object):
    def __init__(self):
        pass

    def update(self, entities, spriteGroup, lsrimg, plr):
        for entity in entities:
            if entity.has('Fire'):
                if entity.Fire.fire and not entity.Fire.over:
                    entity.Fire.over = True
                    # TODO fix inaccurate laser placement
                    laser = Entity('laser', DirtySprite(lsrimg, lsrimg.get_rect(x = plr.DirtySprite.rect.x + plr.DirtySprite.rect.width / 2 - lsrimg.get_width() / 2, y = plr.DirtySprite.rect.y + plr.DirtySprite.rect.height / 2 - lsrimg.get_height() / 2)), Speed(12, 6, 0.1), Movement(), AIControl(), Laser())
                    laser.DirtySprite.angle = plr.DirtySprite.angle
                    laser.DirtySprite.image = pygame.transform.rotate(laser.DirtySprite.ogimage, laser.DirtySprite.angle)
                    laser.DirtySprite.dx = laser.Speed.maxspd * math.cos(math.radians(laser.DirtySprite.angle + 90))
                    laser.DirtySprite.dy = laser.Speed.maxspd * math.sin(math.radians(laser.DirtySprite.angle - 90))
                    entities.append(laser)
                    spriteGroup.add(laser.DirtySprite)
                elif entity.Fire.over:
                    entity.Fire.overt += 1

                if entity.Fire.overt == entity.Fire.overtm:
                    entity.Fire.overt = 0
                    entity.Fire.over = False

        return entities, spriteGroup

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

    def sort(self, entitydict, entities): # might not want to pass all entities each frame
        for entity in entities:
            for component in entity.cs: # inefficient but functional
                if component not in entitydict.keys():
                    entitydict[component] = []
                elif entity not in entitydict[component]:
                    entitydict[component].append(entity)
        return entitydict

    def get(self, entitydict, *types):
        entities = []
        for type in types:
            if type in entitydict.keys():
                entities.extend(entitydict[type])
        return entities

    def destroy(self, entitydict, entities, spriteGroup, *entityinstances):
        for entity in entityinstances:
            for component in entity.cs:
                entitydict[component].remove(entity)
            entities.remove(entity)
            spriteGroup.remove(entity.DirtySprite)
        return entitydict, entities, spriteGroup

class AlienGeneratorSystem(object):
    def __init__(self):
        pass

    def gen(self, entities, alimg, screenrect, spriteGroup):
        if random.randint(0, 120) == 11: # determines rate of gen
            alien = Entity('alien', DirtySprite(alimg, alimg.get_rect(x = random.randint(0, screenrect.width - alimg.get_width()), y = random.randint(0, screenrect.height - alimg.get_height()))), Speed(3, 6, 0.01), Movement(), AIControl(), Alien())
            alien.DirtySprite.dx = random.randint(-alien.Speed.maxspd, alien.Speed.maxspd)
            alien.DirtySprite.dy = random.randint(-alien.Speed.maxspd, alien.Speed.maxspd)
            entities.append(alien)
            spriteGroup.add(alien.DirtySprite)
        return entities, spriteGroup
    
class JetAnimationSystem(object):
    def __init__(self):
        pass
    
    def update(self, entities, player, screen):
        for entity in entities:
            if entity.has('JetAnimation'):
                entity.JetAnimation.rect1 = pygame.Rect(player.DirtySprite.rect.x + player.DirtySprite.rect.width / 7, player.DirtySprite.rect.y + player.DirtySprite.rect.height, entity.JetAnimation.currentimg.get_width(), entity.JetAnimation.currentimg.get_height())
                entity.JetAnimation.rect2 = pygame.Rect(player.DirtySprite.rect.x + player.DirtySprite.rect.width - player.DirtySprite.rect.width / 7, player.DirtySprite.rect.y + player.DirtySprite.rect.height, entity.JetAnimation.currentimg.get_width(), entity.JetAnimation.currentimg.get_height())

                screen.blit(entity.JetAnimation.currentimg, entity.JetAnimation.rect1)
                screen.blit(entity.JetAnimation.currentimg, entity.JetAnimation.rect2)
                pygame.display.update([entity.JetAnimation.rect1, entity.JetAnimation.rect2])
                
                entity.JetAnimation.currentimg = entity.JetAnimation.imgs[0 if entity.JetAnimation.imgindex + 1 > len(entity.JetAnimation.imgs) - 1 else entity.JetAnimation.imgindex + 1]

# Now we must intepret the potential on the map, and create the virtual circles
# The enemies can then try and pathfind their way to the most attractive spots
# In this case, the outer part of the player circle is attractive
# Use slope for pathfinding atm, perhaps A* later if there is obstacles
# Thus, all enemies will attempt to stay at a fixed distance circle away from the player
# Obviously, diff enemy types can interpret the potential fields differently
# Also, they can directly alter the potential field in some classes
# Adding negative potential to enemies could help stop them from clustering around each other too much
# Again, there are many interesting possibilities for the enemy types
# It all depends on how well this does performance wise, which it should work perfectly fine for this game, even unoptimized
class PotentialFieldSystem(object):
    def __init__(self):
        pass

    def map(self, entities):
        map = []
        for entity in entities:
            if entity.has('PotentialField', 'DirtySprite'):
                for i in range(len(entity.PotentialField.potential)):
                    map.append({entity.id: [entity.DirtySprite.rect.center, entity.PotentialField.potential[i]]})
        return map

class AISystem(object): # Control and process enemies here
    def __init__(self):
        pass

    def process(self, map, entities):
        player = []
        for dict in map:
            if 'player' in dict:
                player.append(dict)
        for entity in entities:
            if entity.has('PotentialField', 'DirtySprite'):
                pass
                #for p in map:
                    #pass # implement this later, for now just revolve around the player
                # path = (entity.DirtySprite.rect.centerx -
