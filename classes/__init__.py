"""
This package contains the classes to represent the environment, including Direction, Cell, Grid and Agent.

Classes:
    - Direction: An enumeration class to represent the directions.
    - Cell: A cell with x and y coordinates. Can be blocked (wall) or unblocked.
    - Grid: A 2D grid containing cells.
    - Agent: An agent in the grid.
"""
__all__ = ["Direction", "Cell", "Grid", "Agent"]

from .agent import *