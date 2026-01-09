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
        return x % self.__width, y % self.__height

    def get_agent(self, location: Location):
        return self.__grid.get(location)

    def set_agent(self, location: Location, agent):
        x, y = self.wrap(location.x, location.y)
        loc = Location(x, y)
        self.__grid[loc] = agent
        agent.x = x
        agent.y = y

    def move_agent(self, agent, new_location: Location):
        old_loc = Location(agent.x, agent.y)
        if old_loc in self.__grid:
            del self.__grid[old_loc]

        self.set_agent(new_location, agent)
