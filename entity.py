class Entity():
    def __init__(self, id, **kwargs):
        self.id = id
        for arg in kwargs:
            self.cs.arg = kwargs[arg]
