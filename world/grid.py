class Grid:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.cells = [[None for _ in range(width)] for _ in range(height)]

    def wrap_position(self, x, y):
        return x % self.width, y % self.height

    def place(self, entity, x, y):
        x, y = self.wrap_position(x, y)
        self.cells[y][x] = entity
        entity.x = x
        entity.y = y
