from agents.predator import Predator

class Dek(Predator):
    def __init__(self):
        super().__init__("Dek")
        self.carrying_thia = False

    def hunt(self, monster):
        if monster.health > 0:
            monster.health -= 20
            self.honour += 5
