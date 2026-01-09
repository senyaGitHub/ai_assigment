import random

from world.enviroment import Environment
from agents.location import Location
from agents.dek import Dek
from agents.thia import Thia
from agents.monster import Monster
from agents.wildlife import Wildlife
from gui.gui import Gui
from controller.config import Config

class Simulator:
    def __init__(self):
        self._environment = Environment()
        self._agents = []
        self._step_count = 0
        self._generate_initial_population()

        agent_colours = {
            Dek: "green",
            Thia: "blue",
            Monster: "red",
            Wildlife: "orange"
        }

        self._gui = Gui(self._environment, agent_colours)
        self._running = True

    def _random_empty_location(self):
        """Find a random empty location on the grid"""
        attempts = 0
        max_attempts = 1000

        while attempts < max_attempts:
            x = random.randint(0, self._environment.get_width() - 1)
            y = random.randint(0, self._environment.get_height() - 1)
            loc = Location(x, y)

            if self._environment.get_agent(loc) is None:
                return loc

            attempts += 1

        return None

    def _generate_initial_population(self):
        """Create initial agents"""
        # Create Dek (player character)
        for _ in range(Config.initial_deks):
            dek = Dek()
            loc = self._random_empty_location()
            if loc:
                self._environment.set_agent(loc, dek)
                self._agents.append(dek)

        # Create Thia (damaged synthetic)
        for _ in range(Config.initial_thias):
            thia = Thia()
            loc = self._random_empty_location()
            if loc:
                self._environment.set_agent(loc, thia)
                self._agents.append(thia)

        # Create Monsters (threats)
        for _ in range(Config.initial_monsters):
            monster = Monster()
            loc = self._random_empty_location()
            if loc:
                self._environment.set_agent(loc, monster)
                self._agents.append(monster)

        # Create Wildlife (minor threats/prey)
        species_names = ["Stalker", "Prowler", "Scavenger", "Hunter"]
        for i in range(Config.initial_wildlife):
            wildlife = Wildlife(species=species_names[i % len(species_names)])
            loc = self._random_empty_location()
            if loc:
                self._environment.set_agent(loc, wildlife)
                self._agents.append(wildlife)

    def _step(self):
        """Execute one simulation step"""
        if not self._running or self._gui.is_closed():
            return

        self._step_count += 1

        # Shuffle agents for fairness
        alive_agents = [a for a in self._agents if a.is_alive()]
        random.shuffle(alive_agents)

        # Let each agent act
        for agent in alive_agents:
            if agent.is_alive():
                action, details = agent.act(self._environment)
                self._gui.log_action(agent.name, action, details)

        # Remove dead agents from grid
        removed = self._environment.remove_dead_agents()
        if removed > 0:
            self._gui.log_action("System", "cleanup", f"Removed {removed} dead agents")

        # Check win/lose conditions
        self._check_game_state()

        # Update display
        self._gui.render()

        # Schedule next step (800ms for readability)
        self._gui.after(800, self._step)

    def _check_game_state(self):
        """Check for win/lose conditions"""
        from agents.dek import Dek
        from agents.monster import Monster

        dek_alive = any(isinstance(a, Dek) and a.is_alive() for a in self._agents)
        monsters_alive = any(isinstance(a, Monster) and a.is_alive() for a in self._agents)

        if not dek_alive:
            self._gui.log_action("GAME OVER", "defeat", "Dek has fallen!")
            self._running = False
        elif not monsters_alive and self._step_count > 10:
            self._gui.log_action("VICTORY", "success", "All monsters defeated!")
            self._running = False

    def run(self):
        """Start the simulation"""
        self._gui.log_action("System", "start", "Simulation initialized")
        self._step()
        self._gui.mainloop()
