"""
This package contains the implementation of the algorithms used in the project.

The algorithms are divided into two categories: uninformed and informed.

Uninformed search algorithms:
    - Breadth-First Search (BFS)
    - Depth-First Search (DFS)
    - Iterative Deepening Depth-First Search (IDDFS)

Informed search algorithms:
    - A* Search (Astar)
    - Greedy Best-First Search (Greedy)
    - Bidirectional A* Search (Bidirectional)
"""
uninformed = ["bfs", "dfs", "iddfs"]
informed = ["astar", "greedy", "bidirectional"]

__all__ = uninformed + informed

from . import bfs
from . import dfs
from . import astar
from . import greedy
from . import iddfs
from . import bidirectional