from agents.agent import Agent


class Monster(Agent):
    def __init__(self):
        super().__init__("Adversary", health=200)
