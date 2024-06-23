from .cell import *


class Grid:
    """
    A 2D grid containing cells.

    ### Attributes:
        - height (int): The height of the grid.
        - width (int): The width of the grid.
        - grid (list[list[Cell]]): A 2D list of cells representing the grid.

    ### Methods:
        - is_valid(self, x, y) -> bool: Check if the cell at the given coordinates is valid.
        - get_cell(self, location) -> Cell: Get the cell at the given coordinates.
        - get_neighbor(self, cell, direction, distance - optional) -> Cell: Get the neighbor of the cell at the given direction and distance.
        - get_neighbors(self, cell, can_jump - optional) -> list[Cell]: Get all neighbors of the given cell.
        - reset(self): Reset all cells in the grid.

    ### Properties:
        - size (tuple[int, int]): Return the size of the grid as a tuple (height, width).
        - net_area (int): Calculate the net area of the grid (total area - blocked area).
    """
    def __init__(self, size: tuple[int, int], walls: list[tuple[int, int, int, int]]):
        self.height, self.width = size
        # Create a 2D list of cells
        self.grid = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        # Set the blocked status of the cells based on the walls
        for wall in walls:
            start_x, start_y, width, height = wall
            for row in range(start_y, start_y + height):
                for col in range(start_x, start_x + width):
                    self.grid[row][col].blocked = True

    def is_valid(self, x:int, y:int) -> bool:
        """
        Check if the cell at the given coordinates is valid.
        
        ### Args:
            - x (int): The x coordinate.
            - y (int): The y coordinate.
        
        ### Returns:
            - bool: True if the cell is valid, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, location:tuple[int, int]) -> Cell:
        """
        Get the cell at the given coordinates.
        
        ### Args:
            - location (tuple[int, int]): The coordinates of the cell.
            
        ### Returns:
            - Cell: The cell at the given coordinates.
        """
        x, y = location
        return self.grid[y][x]
    
    def get_neighbor(self, cell:Cell, direction:Direction, distance:int=1) -> Cell | None:
        """
        Get the neighbor of the cell at the given direction and distance.

        ### Args:
            - cell (Cell): the cell to get the neighbor from.
            - direction (Direction): the direction of the neighbor.
            - distance (int, optional): the distance from the original cell. Defaults to 1.

        ### Returns:
            - Cell: the neighbor cell if it is valid, None otherwise.
        """
        x = y = -1
        if direction == Direction.UP:
            x, y = cell.x, cell.y - distance
        elif direction == Direction.LEFT:
            x, y = cell.x - distance, cell.y
        elif direction == Direction.DOWN:
            x, y = cell.x, cell.y + distance
        else: # direction == Direction.RIGHT
            x, y = cell.x + distance, cell.y
        if self.is_valid(x, y):
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell:Cell, can_jump:bool=False) -> list[Cell]:
        """
        Get all neighbors of the given cell. If can_jump is True, allow movement with distance greater than 1.
        
        ### Args:
            - cell (Cell): The cell to get the neighbors from.
            - can_jump (bool, optional): Whether to allow movement with distance greater than 1. Defaults to False.
        
        ### Returns:
            - list[Cell]: A list of neighbor cells. Empty list if no neighbors are found.
        """
            
        neighbors = []
        max_f = cell.f
        # print(f"Cell: {cell} - f: {cell.f}")
        # Add neighbors IN ORDER (up, left, down, right) around the cell
        for direction in list(Direction):
            distance = 1
            neighbor = self.get_neighbor(cell, direction, distance)
            while neighbor is not None:
                if neighbor.g > 0:
                    neighbor_f = neighbor.jump_cost(cell) + neighbor.h
                    if neighbor_f > max_f and distance > 2:
                        # print(f"Neighbor {neighbor} has higher f value {neighbor_f} ({neighbor.jump_cost(cell)} + {neighbor.h}) than the minimum f value {max_f}; Cell: {cell}, jump cost {neighbor.jump_cost(cell)}.")
                        break
                    if neighbor.parent is not None:
                        max_f = neighbor_f
                if not neighbor.blocked:
                    neighbors.append(neighbor)
                if not can_jump:
                    break
                distance += 1
                neighbor = self.get_neighbor(cell, direction, distance)
        # neighbors = [self.get_neighbor(cell, direction) for direction in list(Direction)]
        
        # for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        #     if self.is_valid(cell.x + dx, cell.y + dy):
        #         neighbors.append(self.grid[cell.y + dy][cell.x + dx])

        # for x in range(-1, 2):  # Loop through the 3x3 grid around the cell
        #   for y in range(-1, 2):
        #     if x == 0 and y == 0:
        #       continue
        #     if self.is_valid(cell.x + x, cell.y + y):
        #       neighbors.append(self.grid[cell.y + y][cell.x + x])

        return neighbors

    def reset(self) -> None:
        """
        Reset all cells in the grid.
        """
        for row in self.grid:
            for cell in row:
                cell.reset()

    @property
    def size(self) -> tuple[int, int]:
        """
        Return the size of the grid as a tuple (height, width).
        """
        return self.height, self.width

    @property
    def net_area(self) -> int:
        """
        Calculate the net area of the grid (total area - blocked area).
        """
        return self.height * self.width - sum(cell.blocked for row in self.grid for cell in row)
    