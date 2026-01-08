from world.grid import Grid
from agents.dek import Dek
from agents.monster import Monster
from agents.thia import Thia

class SimulationEngine:
    def __init__(self):
        self.grid = Grid()
        self.dek = Dek()
        self.monster = Monster()
        self.thia = Thia()

        self.grid.place(self.dek, 1, 1)
        self.grid.place(self.thia, 2, 1)
        self.grid.place(self.monster, 10, 10)

    def step(self):
        self.dek.move(1, 0, self.grid)

        if abs(self.dek.x - self.monster.x) <= 1:
            self.dek.hunt(self.monster)
            self.monster.attack(self.dek)

    def get_entities(self):
        return [
            self.dek,
            self.thia,
            self.monster
                ]


    def run(self, steps=50):
        for i in range(steps):
            if not self.dek.is_alive():
                print("Dek has fallen.")
                break
            self.step()
            print(f"Step {i}: Dek HP={self.dek.health}, Honour={self.dek.honour}")
