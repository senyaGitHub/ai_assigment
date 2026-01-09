from agents.agent import Agent
from agents.location import Location
from controller.config import Config
import random

class Wildlife(Agent):
    def __init__(self, species="Creature"):
        super().__init__(species, health=30, stamina=80)
        self.species = species

    def attack(self, target):
        """Wildlife defensive attack"""
        if not self.use_stamina(Config.attack_stamina_cost):
            return False, "Not enough stamina"

        damage = Config.wildlife_attack_damage
        target.take_damage(damage)
        return True, f"Dealt {damage} damage"

    def act(self, environment):
        """Wildlife AI: Flee from predators or wander"""
        from agents.dek import Dek
        from agents.monster import Monster

        nearest_threat = self.find_nearest_agent(environment, Dek)
        if not nearest_threat:
            nearest_threat = self.find_nearest_agent(environment, Monster)

        if nearest_threat:
            threat, threat_loc = nearest_threat
            distance = Location(self.x, self.y).distance_to(threat_loc)

            if distance <= 3:
                if self.is_adjacent(threat) and random.random() < 0.3:
                    success, msg = self.attack(threat)
                    return "attack", f"Defensive attack on {threat.name}"
                else:
                    # Flee
                    if self.use_stamina(Config.move_stamina_cost):
                        self.move_away(threat_loc, environment)
                        return "move", f"Fleeing from {threat.name}"

        if random.random() < 0.5 and self.use_stamina(Config.move_stamina_cost):
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            new_loc = Location(self.x + dx, self.y + dy)
            environment.move_agent(self, new_loc)
            return "move", "Wandering"

        self.rest()
        return "rest", "Resting"
