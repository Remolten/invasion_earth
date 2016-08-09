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

# TODO certain components should require other components to be implemented

from pygame.sprite import DirtySprite

from simpyl import Component

class DirtySprite(DirtySprite, Component):
    def __init__(self, img, rect):
        super().__init__()
        self.id = 'DirtySprite'
        self.image = img
        self.ogimage = img # For rotations
        self.imgs = [] # For animated sprites
        self.imgindex = 0
        self.rect = rect
        self.angle = 0 # Rotation of the sprite, rect will be off
        self.dx = 0 # These are for momentum
        self.dy = 0
        self.ratio = 1
        self.dirty = 1 # Hack to make it show initially

class Speed(Component):
    def __init__(self, maxspd, rotspd, thrust):
        self.id = 'Speed'
        self.maxspd = maxspd
        self.rotspd = rotspd
        self.thrust = thrust

class PlayerControl(Component):
    def __init__(self):
        self.id = 'PlayerControl'
        self.up = False
        self.dwn = False
        self.lft = False
        self.rgt = False

class Health(Component):
    def __init__(self, hlth):
        self.id = 'Health'
        self.health = hlth
        self.damage = 0

class Fire(Component):
    def __init__(self, overtm):
        self.id = 'Fire'
        self.fire = False
        self.over = False
        self.overtm = overtm
        
class Shield(Component):
    def __init__(self, active):
        self.id = 'Shield'
        self.active = active
        self.shield = None

class Flash(Component):
    def __init__(self, flashcd):
        self.id = 'Flash'
        self.flash = False
        self.over = False
        self.flashcd = flashcd
        self.flashx = 0
        self.flashy = 0

class PotentialField(Component):
    def __init__(self, *potentials): # supply lists of potential # + circle radius, order matters
        self.id = 'PotentialField'
        self.potential = []
        for potential in potentials:
            self.potential.append(potential)
            
class JetAnimation(Component):
    def __init__(self, pos, attachedEntityID, freq):
        self.id = 'JetAnimation'
        self.pos = pos # AKA is this the left or right trail, == to 0 or 1 respectively
        self.attachedid = attachedEntityID
        self.freq = freq # AKA change image every freq frames
        self.freqct = 0
        
class Alive(Component):
    def __init__(self):
        self.id = 'Alive'
        self.alive = True

# Placeholder classes for easier identification
class Movement(Component):
    def __init__(self):
        self.id = 'Movement'

class Collision(Component):
    def __init__(self):
        self.id = 'Collision'

class Events(Component):
    def __init__(self):
        self.id = 'Events'

class AIControl(Component):
    def __init__(self):
        self.id = 'AIControl'

class Alien(Component):
    def __init__(self):
        self.id = 'Alien'

class Laser(Component):
    def __init__(self):
        self.id = 'Laser'
        
class Player(Component):
    def __init__(self):
        self.id = 'Player'
