from pygame.sprite import DirtySprite

class DirtySprite(DirtySprite):
    def __init__(self, img, rect):
        super(DirtySprite, self).__init__()
        self.id = 'DirtySprite'
        self.image = img
        self.rect = rect
        self.dirty = 1

class Speed():
    def __init__(self, spd):
        self.id = 'Speed'
        self.spd = spd

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
        self.frng = False
        self.ovrhtd = False

class Flash():
    def __init__(self):
        self.id = 'Flash'
        self.flsh = False
        self.flshcd = False
        self.flshct = 0
