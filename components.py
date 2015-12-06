from pygame_sdl2.sprite import DirtySprite

class DirtySprite(DirtySprite):
    def __init__(self, **kwargs):
        self.id = 'DirtySprite'
        self.img = img
        self.rect = rect
        self.dirty = 0

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
