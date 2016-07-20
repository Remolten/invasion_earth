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

from pygame.sprite import DirtySprite

class DirtySprite(DirtySprite):
    def __init__(self, img, rect):
        super(DirtySprite, self).__init__()
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

class Speed(object):
    def __init__(self, maxspd, rotspd, thrust):
        self.id = 'Speed'
        self.maxspd = maxspd
        self.rotspd = rotspd
        self.thrust = thrust

class PlayerControl(object):
    def __init__(self):
        self.id = 'PlayerControl'
        self.up = False
        self.dwn = False
        self.lft = False
        self.rgt = False

class Health(object):
    def __init__(self, hlth):
        self.id = 'Health'
        self.hlth = hlth

class Fire(object):
    def __init__(self):
        self.id = 'Fire'
        self.fire = False
        self.over = False
        self.overt = 0
        self.overtm = 20 #To be tweaked

class Flash(object):
    def __init__(self):
        self.id = 'Flash'
        self.flsh = False
        self.flshcd = False
        self.flshct = 0

class PotentialField(object):
    def __init__(self, *potentials): # supply lists of potential # + circle radius, order matters
        self.id = 'PotentialField'
        self.potential = []
        for potential in potentials:
            self.potential.append(potential)
            
class JetAnimation(object):
    def __init__(self, pos, attachedEntityID):
        self.id = 'JetAnimation'
        self.pos = pos # AKA is this the left or right trail, == to 0 or 1 respectively
        self.attachedid = attachedEntityID

# Placeholder classes for easier EGS grouping and/or identification
class Movement(object):
    def __init__(self):
        self.id = 'Movement'

class Events(object):
    def __init__(self):
        self.id = 'Events'

class AIControl(object):
    def __init__(self):
        self.id = 'AIControl'

class Alien(object):
    def __init__(self):
        self.id = 'Alien'

class Laser(object):
    def __init__(self):
        self.id = 'Laser'
