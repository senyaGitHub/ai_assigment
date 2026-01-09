import random
from agents.location import Location

class Agent:
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.x = 0
        self.y = 0

    def is_alive(self):
        return self.health > 0

    def act(self, environment):
        """Default behavior: move randomly"""
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        new_x = self.x + dx
        new_y = self.y + dy
        environment.move_agent(self, Location(new_x, new_y))
