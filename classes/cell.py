from .direction import Direction


class Cell:
    """
    A cell with x and y coordinates. Can be blocked (wall) or unblocked.

    ### Attributes:
        - x (int): The x coordinate of the cell.
        - y (int): The y coordinate of the cell.
        - parent (Cell): The parent cell of the current cell.
        - g (int): The distance from the start node.
        - h (int): The distance from the end node.
        - blocked (bool): The blocked status of the cell.

    ### Methods:
        - __eq__(self, other) -> bool: Compare the cell with another cell based on their locations.
        - __hash__(self): Return the hash value of the cell.
        - __sub__(self, other) -> str: Get the direction from the current cell to another.
        - __repr__(self): Return the string representation
        - manhattan_distance(self, other) -> int: Calculate the Manhattan distance between current cell and another cell.
        - jump_cost(self, other) -> int: Calculate the jump cost between the current cell and another cell.
        - reset(self): Reset the cell properties.

    ### Properties:
        - location -> tuple[int, int]: Return the location of the cell as a tuple (x, y).
        - f -> int: Calculate the total cost of the cell - sum of g and h.
    """
    def __init__(self, x: int, y: int, parent: 'Cell' = None):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.parent = parent    # Parent cell
        self.g = 0  # Distance from start node
        self.h = 0  # Distance from end node
        # self.f = 0  # Total cost
        self.blocked = False  # Blocked status

    def __eq__(self, other: 'Cell'):
        """
        Compare the cell with another cell based on their locations.
        """
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        Return the hash value of the cell.
        """
        return hash((self.x, self.y))

    def __sub__(self, other: 'Cell') -> Direction:
        """
        Subtract the x and y coordinates of another cell from the x and y coordinates of this cell to find the direction from the other to this.

        ### Returns:
            - Direction: The direction from the other cell to this cell.
        """
        dx, dy = self.x - other.x, self.y - other.y
        if dx == 0:
            return Direction.UP if dy < 0 else Direction.DOWN
        return Direction.LEFT if dx < 0 else Direction.RIGHT

    def __repr__(self) -> str:
        """
        Return the string representation of the cell.
        """
        return f"<Cell ({self.x}, {self.y})>"

    def __lt__(self, other: 'Cell') -> bool:
        """
        Compare the cell with another cell based on their total cost.
        """
        return self.f < other.f

    def __gt__(self, other: 'Cell') -> bool:
        """
        Compare the cell with another cell based on their total cost.
        """
        return self.f > other.f

    def manhattan_distance(self, other:'Cell') -> int:
        """
        Calculate the Manhattan distance between the current cell and another cell.
        
        ### Args:
            - other (Cell): The other cell.
        
        ### Returns:
            - int: The Manhattan distance between the two cells.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def jump_cost(self, other:'Cell') -> int:
        """
        Calculate the jump cost between the current cell and another cell.
        
        ### Args:
            - other (Cell): The other cell.
        
        ### Returns:
            - int: The jump cost between the two cells.
        """
        distance = self.manhattan_distance(other)
        return 2**(distance - 1)
    
    # def heuristic(self, goal:'Cell', can_jump:bool=False) -> int:
    #     """
    #     Calculate the heuristic value (h) of the cell based on the goal cell.
        
    #     ### Args:
    #         - goal (Cell): The goal cell.
    #         - can_jump (bool, optional): True if the agent can jump over obstacles; False otherwise. Defaults to False.
        
    #     ### Returns:
    #         - int: The heuristic value (h) of the cell.
    #     """
    #     if can_jump:
    #         if self.x == goal.x or self.y == goal.y:
    #             return self.jump_cost(goal)
    #         cell = Cell(goal.x, self.y)
    #         # print(cell)
    #         return self.jump_cost(cell) + cell.jump_cost(goal)
    #     return self.manhattan_distance(goal)

    def reset(self):
        """
        Reset the cell properties.
        """
        self.g = self.h = 0
        self.parent = None

    @property
    def location(self):
        """
        Return the location of the cell as a tuple (x, y).
        """
        return self.x, self.y

    @property
    def f(self):
        """
        Calculate the total cost of the cell - sum of g and h.
        """
        return self.g + self.h
    