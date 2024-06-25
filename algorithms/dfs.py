"""
Depth-First Search (DFS) Algorithm (uninformed)

## Functions:
    - search(agent:Agent, all:bool=False) -> dict[str, list[str] | Cell | int] | int: Perform depth-first search to find a path (not necessarily the shortest) from the agent's location to one of the goals (not necessarily the nearest) or all goals.

## Main idea:
    The depth-first search algorithm is an uninformed search algorithm that explores the deepest nodes in the search tree first. It uses a stack to keep track of the nodes to be explored.

    For each cell, the algorithm explores all its neighbors in reverse order (right, down, left, up) and adds them to the stack if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the stack is empty.
    
    The algorithm can be used to find a path to one of the goals or all goals in the grid. If the agent can jump over obstacles, the algorithm will consider all valid neighbors of the current cell, regardless of their costs.
"""
from collections import deque
from classes import *


def search(agent:Agent, all:bool=False) -> dict[str, list[str] | Cell | int] | int:
    """
    Perform depth-first search to find the shortest path from the agent's location to one of the goals (not necessarily the nearest).

    ### Args:
        - agent (Agent): The agent object. Can or cannot jump over obstacles.
        - all (bool, optional): True to find the shortest path to all goals; False to find the shortest path to one of the goals. Defaults to False.

    ### Returns:
        - If a path is found:
            - dict: A dictionary to store the result of the search with the following keys:
                - 'path' (list[str]): A list of directions (up, left, down, right) to reach the goal.
                - 'goal' (Cell): The goal cell reached.
                - 'count' (int): The number of cells visited during the search.
        - If no path is found:
            - int: The number of cells visited during the search.
    """
    agent.grid.reset()
    start = agent.cell
    # If we only need one goal and the start cell is a goal, return an empty path immediately
    if not all and start in agent.goals:
        return {
            'path': [],
            'goal': start,
            'count': 1
        }
        
    stack = deque([start])
    visited = {start}

    # Initialize the items of the result dictionary
    count = 1  # Start with 1 for the start cell
    path = []
    goals = set(agent.goals)
    reached_goals = set()

    while stack:
        # Pop the last cell from the stack
        current = stack.pop()
        # If the current cell is a goal, tell the agent to return the path
        if current in goals:
            reached_goals.add(current)
            goals.remove(current)
            path.extend(agent.trace_path(current))
            # If we only need one goal or all goals are reached, return the result immediately
            if not all or not goals:
                return {
                    'path': path,
                    'goal': reached_goals if all else current,
                    'count': count
                }

            # Reset the search state for the next goal
            stack = deque([current])
            visited = {current}
            current.parent = None
            continue

        # print("Current:", current.location, "- Stack:", [cell.location for cell in stack], "- Neighbors: ", end="")

        # Explore all valid neighbors of the current cell (in reverse order to maintain the same direction priority order as BFS)
        for neighbor in agent.grid.get_neighbors(current, agent.can_jump)[::-1]:
            if neighbor not in visited:
                # Increment the counter for each visited cell
                count += 1
                # Insert the neighbor at the beginning of the stack (LIFO)
                stack.append(neighbor)
                visited.add(neighbor)
                neighbor.parent = current
                # print(neighbor.location, end=" ")
        # print()
    # If no path is found, return the count of visited cells
    return count
