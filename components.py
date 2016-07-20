from pygame.sprite import DirtySprite

class DirtySprite(DirtySprite):
    def __init__(self, img, rect):
        super(DirtySprite, self).__init__()
        self.id = 'DirtySprite'
        self.image = img
        self.ogimage = img # For rotations
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
    def __init__(self, rect, *images):
        self.id = 'JetAnimation'
        self.imgs = []
        for image in images:
            self.imgs.append(image)
            
        self.rect1 = rect
        self.rect2 = rect
        self.imgindex = 0
        self.currentimg = self.imgs[self.imgindex]

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
