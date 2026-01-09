from agents.location import Location
from controller.config import Config

class Environment:
    def __init__(self, width=Config.grid_width, height=Config.grid_height):
        self.__width = width
        self.__height = height
        self.__grid = {}

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def wrap(self, x, y):
        """Wrap coordinates to create toroidal grid"""
        return x % self.__width, y % self.__height

    def get_agent(self, location: Location):
        """Get agent at location"""
        return self.__grid.get(location)

    def set_agent(self, location: Location, agent):
        """Place agent at location"""
        x, y = self.wrap(location.x, location.y)
        loc = Location(x, y)

        if agent is None:
            if loc in self.__grid:
                del self.__grid[loc]
        else:
            self.__grid[loc] = agent
            agent.x = x
            agent.y = y

    def move_agent(self, agent, new_location: Location):
        """Move agent from current location to new location"""
        old_loc = Location(agent.x, agent.y)
        if old_loc in self.__grid and self.__grid[old_loc] == agent:
            del self.__grid[old_loc]

        x, y = self.wrap(new_location.x, new_location.y)
        new_loc = Location(x, y)

        if new_loc not in self.__grid or self.__grid[new_loc] is None:
            self.set_agent(new_loc, agent)
        else:
            # Location occupied, stay in place
            self.set_agent(old_loc, agent)

    def find_agent(self, agent):
        """Find the location of an agent"""
        return Location(agent.x, agent.y)

    def get_all_agents(self):
        """Get list of all agents in environment"""
        return [agent for agent in self.__grid.values() if agent is not None]

    def remove_dead_agents(self):
        """Remove dead agents from grid"""
        dead_locations = []
        for loc, agent in self.__grid.items():
            if agent and not agent.is_alive():
                dead_locations.append(loc)

        for loc in dead_locations:
            del self.__grid[loc]

        return len(dead_locations)
