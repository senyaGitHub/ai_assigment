from agents.agent import Agent


class Dek(Agent):
    def __init__(self):
        super().__init__("Dek", health=100)
        self.honour = 0
