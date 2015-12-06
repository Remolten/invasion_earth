class Entity():
    def __init__(self, id, *args):
        self.id = id
        self.cs = {}
        for arg in args:
            self.cs[arg.id] = arg
