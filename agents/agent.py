class Agent:
    def __init__(self, name, health, stamina):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.x = 0
        self.y = 0

    def is_alive(self):
        return self.health > 0
