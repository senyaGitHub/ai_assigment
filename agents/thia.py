from agents.agent import Agent

class Thia(Agent):
    def __init__(self):
        super().__init__("Thia", health=50, stamina=0)
        self.damaged = True
        self.can_move = False

    def act(self, environment):
        """Thia cannot move on her own - she's damaged"""

        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + 1)
            return "rest", "Recovering from damage"
        return "idle", "Waiting for help"
