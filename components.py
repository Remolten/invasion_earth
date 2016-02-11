from pygame.sprite import DirtySprite

class DirtySprite(DirtySprite):
    def __init__(self, img, rect):
        super(DirtySprite, self).__init__()
        self.id = 'DirtySprite'
        self.image = img
        self.ogimage = img # For rotations
        self.rect = rect
        self.angle = 0
        self.dirty = 1 # Hack to make it show initially

class Speed():
    def __init__(self, spd, rotspd):
        self.id = 'Speed'
        self.spd = spd
        self.rotspd = rotspd

class PlayerControl():
    def __init__(self):
        self.id = 'PlayerControl'
        self.up = False
        self.dwn = False
        self.lft = False
        self.rgt = False

class Health():
    def __init__(self, hlth):
        self.id = 'Health'
        self.hlth = hlth

class Fire():
    def __init__(self):
        self.id = 'Fire'
        self.fire = False
        self.over = False
        self.overt = 0
        self.overtm = 20 #To be tweaked

class Flash():
    def __init__(self):
        self.id = 'Flash'
        self.flsh = False
        self.flshcd = False
        self.flshct = 0
