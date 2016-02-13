# Components must have unique string ids
# Components are accessed directly eg entity.component
# TODO set id internally?

class Entity(object):
    def __init__(self, id, *components):
        self.id = id
        self.cs = []
        self.add(*components)

    def add(self, *components):
        for component in components:
            self.__dict__[component.id] = component
            self.cs.append(component.id)

    def rem(self, *components):
        for component in components:
            del self.__dict__[component.id]
            self.cs.remove(component.id) #probably syntax is incorrect

    def has(self, *componentstrs):
        for componentstr in componentstrs:
            if not hasattr(self, componentstr):
                return False
        return True
