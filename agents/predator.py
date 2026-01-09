#from agents.agent import Agent

class Predator(Agent):
    def __init__(self, name):
        super().__init__(name, health=100)
        self.stamina = 100
        self.honour = 0

    def move(self, dx, dy, environment):
        if self.stamina <= 0:
            return
        self.stamina -= 1
        new_x = self.x + dx
        new_y = self.y + dy
        environment.move_agent(self, Location(new_x, new_y))
