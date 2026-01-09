from agents.agent import Agent
from agents.location import Location
from controller.config import Config

class Monster(Agent):
    def __init__(self):
        super().__init__("Adversary", health=200, stamina=150)
        self.aggression = 0.8  # 80% chance to pursue

    def attack(self, target):
        """Monster attacks"""
        if not self.use_stamina(Config.attack_stamina_cost):
            return False, "Not enough stamina"

        damage = Config.monster_attack_damage
        target.take_damage(damage)
        return True, f"Dealt {damage} damage"

    def act(self, environment):
        """Monster AI: Pursue and attack Dek or other predators"""
        import random

        # Rest if low stamina
        if self.stamina < 20:
            self.rest()
            return "rest", "Recovering stamina"

        # Find nearest predator (Dek)
        from agents.dek import Dek
        nearest_predator = self.find_nearest_agent(environment, Dek)

        if nearest_predator and random.random() < self.aggression:
            target, target_loc = nearest_predator

            # Attack if adjacent
            if self.is_adjacent(target):
                success, msg = self.attack(target)
                return "attack", f"Attacked {target.name}: {msg}"
            else:
                # Move towards predator
                self.move_towards(target_loc, environment)
                return "move", f"Pursuing {target.name}"

        # Random patrol
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        new_loc = Location(self.x + dx, self.y + dy)

        if self.use_stamina(Config.move_stamina_cost):
            environment.move_agent(self, new_loc)
            return "move", "Patrolling"

        return "idle", "Low stamina"
