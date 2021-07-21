class Game:
    def __init__(self, name, category, console, id=None):
        self.id = id
        self.name = name
        self.category = category
        self.console = console

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password