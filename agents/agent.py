import random
from agents.location import Location



class Agent:
    def __init__(self, name, health, stamina=100):
        self.name = name
        self.max_health = health
        self.health = health
        self.max_stamina = stamina
        self.stamina = stamina
        self.x = 0
        self.y = 0
        self.is_dead = False

    def is_alive(self):
        return self.health > 0 and not self.is_dead

    def take_damage(self, damage):
        """Reduce health by damage amount"""
        self.health = max(0, self.health - damage)
        if self.health <= 0:
            self.is_dead = True

    def use_stamina(self, amount):
        """Use stamina for actions"""
        self.stamina = max(0, self.stamina - amount)
        return self.stamina > 0

    def rest(self):
        """Regenerate stamina"""
        from controller.config import Config
        self.stamina = min(self.max_stamina, self.stamina + Config.stamina_regen)

    def get_health_percentage(self):
        """Get health as percentage"""
        return (self.health / self.max_health) * 100

    def find_nearest_agent(self, environment, agent_type):
        """Find nearest agent of specific type"""
        my_loc = Location(self.x, self.y)
        nearest = None
        min_distance = float('inf')

        for y in range(environment.get_height()):
            for x in range(environment.get_width()):
                loc = Location(x, y)
                agent = environment.get_agent(loc)

                if agent and isinstance(agent, agent_type) and agent.is_alive():
                    distance = my_loc.distance_to(loc)
                    if distance < min_distance and distance > 0:
                        min_distance = distance
                        nearest = (agent, loc)

        return nearest

    def move_towards(self, target_loc, environment):
        """Move one step towards target location"""
        from controller.config import Config

        if not self.use_stamina(Config.move_stamina_cost):
            return False

        my_loc = Location(self.x, self.y)
        dx = 0
        dy = 0

        # Choose direction that reduces distance
        if target_loc.x != self.x:
            dx = 1 if target_loc.x > self.x else -1
        elif target_loc.y != self.y:
            dy = 1 if target_loc.y > self.y else -1

        new_loc = Location(self.x + dx, self.y + dy)
        environment.move_agent(self, new_loc)
        return True

    def move_away(self, threat_loc, environment):
        """Move one step away from threat location"""
        from controller.config import Config

        if not self.use_stamina(Config.move_stamina_cost):
            return False

        dx = 0
        dy = 0

        # Move in opposite direction
        if threat_loc.x != self.x:
            dx = -1 if threat_loc.x > self.x else 1
        elif threat_loc.y != self.y:
            dy = -1 if threat_loc.y > self.y else 1

        new_loc = Location(self.x + dx, self.y + dy)
        environment.move_agent(self, new_loc)
        return True

    def is_adjacent(self, other_agent):
        """Check if another agent is adjacent"""
        return abs(self.x - other_agent.x) + abs(self.y - other_agent.y) == 1

    def act(self, environment):
        """Default behavior: rest if low stamina, else move randomly"""
        if self.stamina < 20:
            self.rest()
            return "rest"

        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        new_loc = Location(self.x + dx, self.y + dy)
        environment.move_agent(self, new_loc)
        return "move"
