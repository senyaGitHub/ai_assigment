from agents.agent import Agent

class Thia(Agent):
    def __init__(self):
        super().__init__("Thia", health=50, stamina=0)
        self.damaged = True

    def give_hint(self):
        return "Adversary detected in nearby sector."
