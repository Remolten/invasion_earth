# Components must have unique string ids
# Components are accessed directly eg entity.component

class Entity():
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
            self.cs.remove(component.id)

    def has(self, *component_strs):
        for component_str in component_strs:
            if not hasattr(self, component_str):
                return False
        return True
