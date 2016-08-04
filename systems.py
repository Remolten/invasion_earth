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

from simpyl import System

from components import *

import math, random

# Utility function which when used via yield will pause for x frames
#def wait(frames):
#    fr = frames
#    while fr > 0:
#        fr -= 1
#        yield fr

# Processes events and changes the relevant values of certain components
class EventSystem(System):
    def __init__(self):
        self.id = "EventSystem"

    def update(self):
        for playerControlComponent, playerControlEntity in enumerate(self.game.getComponents('PlayerControl')):
            for fireComponent, fireEntity in enumerate(self.game.getComponents('Fire')):
                for event in self.events:
                    if event.type == KEYDOWN:
                        if event.key == K_UP or event.key == ord('w'):
                            playerControlComponent.up = True
                            playerControlComponent.dwn = False
                        if event.key == K_DOWN or event.key == ord('s'):
                            playerControlComponent.dwn = True
                            playerControlComponent.up = False
                        if event.key == K_LEFT or event.key == ord('a'):
                            playerControlComponent.lft = True
                            playerControlComponent.rgt = False
                        if event.key == K_RIGHT or event.key == ord('d'):
                            playerControlComponent.rgt = True
                            playerControlComponent.lft = False
                        if event.key == K_SPACE:
                            fireComponent.fire = True

                    if event.type == KEYUP:
                        if event.key == K_UP or event.key == ord('w'):
                            playerControlComponent.up = False
                        if event.key == K_DOWN or event.key == ord('s'):
                            playerControlComponent.dwn = False
                        if event.key == K_LEFT or event.key == ord('a'):
                            playerControlComponent.lft = False
                        if event.key == K_RIGHT or event.key == ord('d'):
                            playerControlComponent.rgt = False
                        if event.key == K_SPACE:
                            fireComponent.fire = False

# The MovementSystem has been ported! It should work fine.
# Unfortunately, the initial design was incredibly flawed
# This means the purity of the ECS is compromised unless we do a huge rewrite of this function
# NOTE For future reference, each system must only deal with one single component, not multiple
class MovementSystem(System):
    def __init__(self):
        self.id = "MovementSystem"

    def update(self):
        for entity in self.game.getEntitiesByComponents('DirtySprite', 'Speed', 'PlayerControl'):
            # Note this is dirty but necessary due to the flawed initial design of this system
            # An ECS should only access one component type per system
            for component in entity.cs:
                if component.id == 'DirtySprite':
                    dsComponent = component
                elif component.id == 'Speed':
                    speedComponent = component
                elif component.id == 'PlayerControl':
                    pcComponent = component
            
            if pcComponent.up:
                dsComponent.dx += speedComponent.maxspd * math.cos(math.radians(dsComponent.angle + 90)) * speedComponent.thrust
                dsComponent.dy += speedComponent.maxspd * math.sin(math.radians(dsComponent.angle - 90)) * speedComponent.thrust
                dsComponent.dirty = 1
            #elif pcComponent.dwn:
                #pass # Not needed unless we add virtual brakes
            if pcComponent.lft:
                dsComponent.angle += speedComponent.rotspd
                dsComponent.image = pygame.transform.rotate(dsComponent.ogimage, dsComponent.angle)
                dsComponent.rect = dsComponent.image.get_rect(center=dsComponent.rect.center)
                dsComponent.dirty = 1
            elif pcComponent.rgt:
                dsComponent.angle -= speedComponent.rotspd
                dsComponent.image = pygame.transform.rotate(dsComponent.ogimage, dsComponent.angle)
                dsComponent.rect = dsComponent.image.get_rect(center=dsComponent.rect.center)
                dsComponent.dirty = 1
            elif dsComponent.dx == 0 and dsComponent.dy == 0:
                dsComponent.dirty = 0
            elif not pcComponent.up: #and not pcComponent.dwn:
                # Add a slight amount of friction
                if dsComponent.dx > 0:
                    dsComponent.dx *= 0.97 #if dsComponent.dx > 0.3 else 0.9
                elif dsComponent.dx < 0:
                    dsComponent.dx *= 0.9
                if dsComponent.dy > 0:
                    dsComponent.dy *= 0.97 #if dsComponent.dy > 0.3 else 0.9
                elif dsComponent.dy < 0:
                    dsComponent.dy *= 0.9
                # You could make a case for letting the ship drift when it gets to low speeds
                # But this just causes an instant drop off when the speed gets low
                if abs(dsComponent.dx) < 0.2:
                    dsComponent.dx = 0
                if abs(dsComponent.dy) < 0.2:
                    dsComponent.dy = 0

        # FUTURE will be broken if we added multiplayer
        for alienEntity in self.game.getEntitiesByComponents('Alien'):
            # NOTE Movement will be wonky if there exists more then one Player1 component
            for p1Entity in self.game.getEntitiesByComponents('Player1'):
                # Here we set the aliens to track the player
                # All we have to do is set the angle to always face the player
                # Get slope and convert to degrees
                yslope = p1Entity.DirtySprite.rect.centery - alienEntity.DirtySprite.rect.centery
                xslope = p1Entity.DirtySprite.rect.centerx - alienEntity.DirtySprite.rect.centerx
                alienEntity.DirtySprite.dx += alienEntity.Speed.maxspd * xslope * alienEntity.Speed.thrust
                alienEntity.DirtySprite.dy += alienEntity.Speed.maxspd * yslope * alienEntity.Speed.thrust

        for laserEntity in self.game.getEntitiesByComponents('Laser'):
            if laserEntity.DirtySprite.rect.x <= 0 or laserEntity.DirtySprite.rect.x >= self.screenrect.width - laserEntity.DirtySprite.rect.width:
                laserEntity.DirtySprite.dx *= -1
            if laserEntity.DirtySprite.rect.y <= 0 or laserEntity.DirtySprite.rect.y >= self.screenrect.height - laserEntity.DirtySprite.rect.height:
                laserEntity.DirtySprite.dy *= -1

            if laserEntity.DirtySprite.dx != 0:
                laserEntity.DirtySprite.angle = 90 - math.degrees(math.atan(laserEntity.DirtySprite.dy / laserEntity.DirtySprite.dx))
            elif laserEntity.DirtySprite.dy == 0:
                laserEntity.DirtySprite.angle = 90 if laserEntity.DirtySprite.dx > 0 else 270
            else:
                laserEntity.DirtySprite.angle = 0 if laserEntity.DirtySprite.dy > 0 else 180

            laserEntity.DirtySprite.image = pygame.transform.rotate(laserEntity.DirtySprite.ogimage, laserEntity.DirtySprite.angle)
            laserEntity.DirtySprite.rect = laserEntity.DirtySprite.image.get_rect(center=laserEntity.DirtySprite.rect.center)

        # TODO Change this and above in this function to instead be put in the simpyl library directly eg have a simpyl function return a dict in the form {entity: [components]}
        for entity in self.game.getEntitiesByComponents('DirtySprite', 'Speed'):
            # Note this is dirty but necessary due to the flawed initial design of this system
            # An ECS should only access one component type per system
            for component in entity.cs:
                if component.id == 'DirtySprite':
                    dsComponent = component
                elif component.id == 'Speed':
                    speedComponent = component
        
            # Keeps speed under maxspd but at the same ratio
            dsComponent.ratio = 1
            if dsComponent.dx > speedComponent.maxspd:
                dsComponent.ratio = speedComponent.maxspd / dsComponent.dx
            elif dsComponent.dx < -speedComponent.maxspd:
                dsComponent.ratio = -speedComponent.maxspd / dsComponent.dx
            if dsComponent.dy > speedComponent.maxspd:
                dsComponent.ratio = speedComponent.maxspd / dsComponent.dy
            elif dsComponent.dy < -speedComponent.maxspd:
                dsComponent.ratio = -speedComponent.maxspd / dsComponent.dy

            # Actually move stuff
            dsComponent.dy *= dsComponent.ratio
            dsComponent.dx *= dsComponent.ratio
            dsComponent.rect.x += dsComponent.dx
            dsComponent.rect.y += dsComponent.dy

            # Keep sprite inside the screen
            dsComponent.rect.clamp_ip(self.screenrect)

# A system which creates lasers for all entities with fire objects
class FireSystem(System):
    def __init__(self):
        self.id = "FireSystem"

    def update(self): 
        for fireComponent, fireEntity in enumerate(self.game.getComponents('Fire')):
            if fireComponent.fire and not fireComponent.over:
                fireComponent.over = True
                # TODO fix inaccurate laser placement
                # Cause: Not sure exactly
                # TODO add optional kwargs for these DirtySprite variable settings in the component
                laser = self.Entity('laser', DirtySprite(self.lsrimg, self.lsrimg.get_rect(x = fireEntity.DirtySprite.rect.x + fireEntity.DirtySprite.rect.width / 2 - self.lsrimg.get_width() / 2, y = fireEntity.DirtySprite.rect.y + fireEntity.DirtySprite.rect.height / 2 - self.lsrimg.get_height() / 2)), Speed(12, 6, 0.1), Movement(), AIControl(), Laser())
                laser.DirtySprite.angle = fireEntity.DirtySprite.angle
                laser.DirtySprite.image = pygame.transform.rotate(laser.DirtySprite.ogimage, laser.DirtySprite.angle)
                laser.DirtySprite.dx = laser.Speed.maxspd * math.cos(math.radians(laser.DirtySprite.angle + 90))
                laser.DirtySprite.dy = laser.Speed.maxspd * math.sin(math.radians(laser.DirtySprite.angle - 90))
                
                # TODO this should be relegated to some sort of internal system
                self.spriteGroup.add(laser.DirtySprite)
            elif fireComponent.over:
                fireComponent.overt += 1

            if fireComponent.overt == fireComponent.overtm:
                fireComponent.overt = 0
                fireComponent.over = False

# This must be revamped to take entity lists, not sprite groups
# FIXME Above definitely still applies
# TODO port this
class DrawSystem(System):
    def __init__(self):
        self.id = "DrawSystem"

    def draw(self, screen, screenrect, bg, *spritegroups):
        screen.fill((0, 0, 0))
        screen.blit(bg, pygame.Rect(0, 0, bg.get_width(), bg.get_height()))
        screen.blit(bg, pygame.Rect(bg.get_width(), 0, bg.get_width(), bg.get_height()))
        screen.blit(bg, pygame.Rect(0, bg.get_height(), bg.get_width(), bg.get_height()))
        screen.blit(bg, pygame.Rect(bg.get_width(), bg.get_height(), bg.get_width(), bg.get_height()))
        rlst = [screenrect]
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
# This is probably not needed anymore now that we use the simpyl framework
#class EntityGroupSystem(System):
#    def __init__(self):
#        pass
#
#    def isort(self, entities):
#        entitydict = {}
#        return self.sort(entitydict, entities)
#
#    def sort(self, entitydict, entities): # might not want to pass all entities each frame
#        for entity in entities:
#            for component in entity.cs: # inefficient but functional
#                if component not in entitydict.keys():
#                    entitydict[component] = []
#                elif entity not in entitydict[component]:
#                    entitydict[component].append(entity)
#        return entitydict
#
#    def get(self, entitydict, *types):
#        entities = []
#        for type in types:
#            if type in entitydict.keys():
#                entities.extend(entitydict[type])
#        return entities
#
#    def destroy(self, entitydict, entities, spriteGroup, *entityinstances):
#        for entity in entityinstances:
#            for component in entity.cs:
#                entitydict[component].remove(entity)
#            entities.remove(entity)
#            spriteGroup.remove(entity.DirtySprite)
#        return entitydict, entities, spriteGroup

# TODO port this
class AlienGeneratorSystem(System):
    def __init__(self):
        self.id = "AlienGeneratorSystem"

    def gen(self, entities, alimg, screenrect, spriteGroup):
        # FIXME Rate of generation needs to be accessible outside of the function (Note: easy)
        if random.randint(0, 120) == 11:
            alien = Entity('alien', DirtySprite(alimg, alimg.get_rect(x = random.randint(0, screenrect.width - alimg.get_width()), y = random.randint(0, screenrect.height - alimg.get_height()))), Speed(3, 6, 0.01), Movement(), AIControl(), Alien())
            alien.DirtySprite.dx = random.randint(-alien.Speed.maxspd, alien.Speed.maxspd)
            alien.DirtySprite.dy = random.randint(-alien.Speed.maxspd, alien.Speed.maxspd)
            entities.append(alien)
            spriteGroup.add(alien.DirtySprite)
        return entities, spriteGroup

# TODO port this thing
class JetAnimationSystem(System):
    def __init__(self):
        self.id = "JetAnimationSystem"
    
    def create(self, entities, attachedEntityID, spriteGroup, jetimgs):
        reqimg = jetimgs[0]
        for i in range(2):
            trail = Entity('jetTrail', DirtySprite(reqimg, reqimg.get_rect()), JetAnimation(i, attachedEntityID, 3))
            trail.DirtySprite.imgs = jetimgs
            trail.DirtySprite.dirty = 2 # Set it to always be repainted because it's animated every frame
            entities.append(trail)
            spriteGroup.add(trail.DirtySprite)
        return entities, spriteGroup
    
    def update(self, entities):
        for entity in entities:
            if entity.has('JetAnimation'):
                if entity.JetAnimation.freqct == entity.JetAnimation.freq:
                    if entity.DirtySprite.imgindex + 1 > len(entity.DirtySprite.imgs) - 1:
                        entity.DirtySprite.imgindex = 0
                    else:
                        entity.DirtySprite.imgindex += 1

                    entity.DirtySprite.image = entity.DirtySprite.imgs[entity.DirtySprite.imgindex]
                    entity.JetAnimation.freqct = 0
                else:
                    entity.JetAnimation.freqct += 1
                
                # Get the entity it is attached to
                attachedToEntity = list(filter(lambda x: x.id == entity.JetAnimation.attachedid, entities))[0]
                
                entity.DirtySprite.image = pygame.transform.rotate(entity.DirtySprite.imgs[entity.DirtySprite.imgindex], attachedToEntity.DirtySprite.angle)
                    
                # Determine position relative to the entity its attached to
                # Use the parametric equation of a circle
                radius = max(attachedToEntity.DirtySprite.rect.width, attachedToEntity.DirtySprite.rect.height) / 1
                x = radius * math.cos(math.radians(attachedToEntity.DirtySprite.angle + 270))
                y = radius * math.sin(math.radians(attachedToEntity.DirtySprite.angle - 270))
                
                if entity.JetAnimation.pos == 0:
#                    entity.DirtySprite.rect = pygame.Rect(attachedToEntity.DirtySprite.rect.x + attachedToEntity.DirtySprite.rect.width / 7, attachedToEntity.DirtySprite.rect.y + attachedToEntity.DirtySprite.rect.height, entity.DirtySprite.image.get_width(), entity.DirtySprite.image.get_height())
                    entity.DirtySprite.rect = pygame.Rect(attachedToEntity.DirtySprite.rect.centerx + x, attachedToEntity.DirtySprite.rect.centery + y, entity.DirtySprite.image.get_width(), entity.DirtySprite.image.get_height())
                else:
                    pass
#                    entity.DirtySprite.rect = pygame.Rect(attachedToEntity.DirtySprite.rect.x + attachedToEntity.DirtySprite.rect.width - attachedToEntity.DirtySprite.rect.width / 7, attachedToEntity.DirtySprite.rect.y + attachedToEntity.DirtySprite.rect.height, entity.DirtySprite.image.get_width(), entity.DirtySprite.image.get_height())
#                    entity.DirtySprite.rect = pygame.Rect(attachedToEntity.DirtySprite.rect.x + x, attachedToEntity.DirtySprite.rect.y + y, entity.DirtySprite.image.get_width(), entity.DirtySprite.image.get_height())


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

# TODO Port these to the new simpyl framework
# Not necessary until they can actually begin being used
#class PotentialFieldSystem(System):
#    def __init__(self):
#        pass
#
#    def map(self, entities):
#        map = []
#        for entity in entities:
#            if entity.has('PotentialField', 'DirtySprite'):
#                for i in range(len(entity.PotentialField.potential)):
#                    map.append({entity.id: [entity.DirtySprite.rect.center, entity.PotentialField.potential[i]]})
#        return map
#
#class AISystem(System): # Control and process enemies here
#    def __init__(self):
#        pass
#
#    def process(self, map, entities):
#        player = []
#        for dict in map:
#            if 'player' in dict:
#                player.append(dict)
#        for entity in entities:
#            if entity.has('PotentialField', 'DirtySprite'):
#                pass
#                #for p in map:
#                    #pass # implement this later, for now just revolve around the player
#                # path = (entity.DirtySprite.rect.centerx -
