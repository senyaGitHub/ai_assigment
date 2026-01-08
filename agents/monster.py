from agents.agent import Agent

class Monster(Agent):
    def __init__(self, name="Adversary"):
        super().__init__(name, health=200, stamina=0)

    def attack(self, target):
        target.health -= 15
