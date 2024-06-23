from .grid import *


class Agent:
    """
    An agent in the grid.

    ### Attributes:
        - grid (Grid): The grid object.
        - cell (Cell): The cell object representing the agent's location.
        - goals (list[Cell]): A list of cell objects representing the goal locations.
        - reached_goals (list[Cell]): A list of cell objects representing the reached goal locations.
        - can_jump (bool): Whether the agent can jump over obstacles.

    ### Methods:
        - trace_path(self, cell:Cell, backward=True) -> list[str]: Given the goal cell, return the path from the start cell to the goal cell as a list of directions (up, down, left, right).
        - get_nearest_goal(self) -> tuple[int, int]: Get the nearest goal to the agent's current location (Manhattan distance).
    """
    def __init__(self, grid:Grid, location:tuple[int, int], goals:list[tuple[int, int]], can_jump=False):
        self.grid = grid
        self.cell = grid.get_cell(location)
        self.goals:list['Cell'] = []
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
            # print(f"Cell: {cell.location} - Parent: {cell.parent.location}")
            distance = cell.manhattan_distance(cell.parent)
            distance_str = f"_{distance}" if self.can_jump else ""
            cost = cell.jump_cost(cell.parent)
            total_cost += cost
            if backward:
                path.insert(0, (cell - cell.parent).value + distance_str)
            else: # Forward
                path.append((cell.parent - cell).value + distance_str)
            cell = cell.parent
        # print(f"Total Cost: {total_cost}")
        return path

    def get_nearest_goal(self, cell:Cell=None) -> Cell:
        """
        Get the nearest goal to the agent's current location (Manhattan distance).
        
        ### Returns:
            - Cell: The nearest goal cell.
        """
        if cell is None:
            cell = self.cell
        return min(self.goals, key=cell.manhattan_distance)
    