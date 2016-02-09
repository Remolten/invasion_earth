# Components must have unique string ids
# Components are accessed directly eg entity.component

class Entity():
    def __init__(self, id, *components):
        self.id = id
        self.cs = []
        for c in components:
            self.__dict__[c.id] = c
            self.cs.append(c.id)
