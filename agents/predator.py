from agents.agent import Agent

class Predator(Agent):
    def __init__(self, name):
        super().__init__(name, health=100, stamina=100)
        self.honour = 0

    def move(self, dx, dy, grid):
        if self.stamina <= 0:
            return
        self.stamina -= 1
        self.x, self.y = grid.wrap_position(self.x + dx, self.y + dy)
