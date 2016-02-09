# Components must have unique string ids
# Components are accessed directly eg entity.component

class Entity():
    def __init__(self, id, *components):
        self.id = id
        for c in components:
            cid = c.id
            self.cid = c
