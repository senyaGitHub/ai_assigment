from agents.agent import Agent


class Thia(Agent):
    def __init__(self):
        super().__init__("Thia", health=50)
        self.damaged = True
