from agents.agent import Agent
from agents.location import Location
from controller.config import Config

class Dek(Agent):
    def __init__(self):
        super().__init__("Dek", health=100, stamina=100)
        self.honour = 0
        self.trophies = 0
        self.carrying_thia = False

    def gain_honour(self, amount, reason=""):
        """Increase honour score"""
        self.honour += amount
        return reason

    def attack(self, target):
        """Attack another agent"""
        if not self.use_stamina(Config.attack_stamina_cost):
            return False, "Not enough stamina"

        damage = Config.dek_attack_damage
        target.take_damage(damage)

        if not target.is_alive():
            # Gain honour for kill
            from agents.monster import Monster
            from agents.wildlife import Wildlife

            if isinstance(target, Monster):
                self.gain_honour(Config.honour_monster_kill, "Killed monster")
                self.trophies += 1
            elif isinstance(target, Wildlife):
                self.gain_honour(Config.honour_wildlife_kill, "Killed wildlife")

        return True, f"Dealt {damage} damage"

    def act(self, environment):
        """Dek's AI: Hunt monsters and wildlife"""
        if self.stamina < 30:
            self.rest()
            return "rest", "Resting to recover stamina"

        from agents.monster import Monster
        nearest_monster = self.find_nearest_agent(environment, Monster)

        if nearest_monster:
            target, target_loc = nearest_monster

            if self.is_adjacent(target):
                success, msg = self.attack(target)
                return "attack", f"Attacked {target.name}: {msg}"
            else:
                self.move_towards(target_loc, environment)
                return "move", f"Moving towards {target.name}"

        from agents.wildlife import Wildlife
        nearest_wildlife = self.find_nearest_agent(environment, Wildlife)

        if nearest_wildlife:
            target, target_loc = nearest_wildlife

            if self.is_adjacent(target):
                success, msg = self.attack(target)
                return "attack", f"Attacked {target.name}: {msg}"
            else:
                self.move_towards(target_loc, environment)
                return "move", f"Moving towards {target.name}"

        self.rest()
        return "rest", "No targets nearby, resting"
