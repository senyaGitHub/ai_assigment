class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Location({self.x}, {self.y})"

    def distance_to(self, other):
            """Calculate Manhattan distance to another location"""
            return abs(self.x - other.x) + abs(self.y - other.y)
