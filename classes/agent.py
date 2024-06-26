from .grid import *


class Agent:
    """
    An agent in the grid.

    ### Attributes:
        - grid (Grid): The grid object.
        - cell (Cell): The cell object representing the agent's location.
        - goals (list[Cell]): A list of cell objects representing the goal locations.
        - can_jump (bool): Whether the agent can jump over obstacles.

    ### Methods:
        - trace_path(self, cell:Cell, backward=True) -> list[str]: Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).
        - traverse_path(self, path:list[str]) -> Cell: Traverse the path from the start cell to the goal cell.
    """
    def __init__(self, grid:Grid, location:tuple[int, int], goals:list[tuple[int, int]], can_jump=False):
        self.grid = grid
        self.cell = grid.get_cell(location)
        self.goals:list[Cell] = []
        for goal in goals:
            cell = self.grid.get_cell(goal)
            self.goals.append(cell)
        self.can_jump = can_jump

    def trace_path(self, cell:Cell, backward=True) -> list[str]:
        """
        Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).

        ### Args:
            - cell (Cell): The goal cell.
            - backward (bool, optional): The direction of the path. True for backward, False for forward. Defaults to True.

        ### Returns:
            - list[str]: A list of directions (up, down, left, right) to reach the goal cell.
        """
        path = []
        total_cost = 0
        while cell.parent:
            distance = cell.manhattan_distance(cell.parent)
            distance_str = f"_{distance}" if self.can_jump else ""
            cost = cell.jump_cost(cell.parent)
            total_cost += cost
            if backward:
                path.insert(0, (cell - cell.parent).value + distance_str)
            else: # Forward
                path.append((cell.parent - cell).value + distance_str)
            cell = cell.parent
        return path
    
    def traverse_path(self, path:list[str]) -> tuple[Cell, int]:
        """
        Traverse the path from the start cell to the goal cell.

        ### Args:
            - path (list[str]): A list of Direction values (up, down, left, right) to reach the goal cell.

        ### Returns:
            - Cell: The goal cell when the agent traverses the path from its cell.
            - int: The total cost of traversing the path.
        """
        current = self.cell
        cost = 0
        for direction_str in path:
            distance = 1
            if "_" in direction_str:
                direction_str, distance_str = direction_str.split("_")
                distance = int(distance_str)
            direction = Direction(direction_str)
            neighbor = self.grid.get_neighbor(current, direction, distance)
            cost += current.jump_cost(neighbor)
            current = neighbor
        return current, cost
