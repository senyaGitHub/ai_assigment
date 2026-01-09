import random

from world.enviroment import Environment
from agents.location import Location
from agents.dek import Dek
from agents.thia import Thia
from agents.monster import Monster
from gui.gui import Gui

class Simulator:
    def __init__(self):
        self._environment = Environment()
        self._agents = []
        self._generate_initial_population()

        agent_colours = {
            Dek: "green",
            Thia: "blue",
            Monster: "red"
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

        agent_types = [Dek, Thia, Monster]
        agents_per_type = 3

        for agent_class in agent_types:
            for _ in range(agents_per_type):
                agent = agent_class()
                loc = self._random_empty_location()

                if loc:
                    self._environment.set_agent(loc, agent)
                    self._agents.append(agent)

    def _step(self):
        """Execute one simulation step"""
        if not self._running or self._gui.is_closed():
            return


        agents_copy = self._agents.copy()
        random.shuffle(agents_copy)


        for agent in agents_copy:
            if agent.is_alive():
                agent.act(self._environment)


        self._gui.render()

        # step scheduler
        self._gui.after(500, self._step)

    def run(self):
        """Start the simulation"""
        self._step()
        self._gui.mainloop()
