"""
A* Search Algorithm (informed)

## Functions:
    - search(agent:Agent, all:bool=False) -> dict[str, list[str] | Cell | int] | int: Perform A* search to find the shortest path from the agent's location to the seemingly nearest goal (estimated based on Manhattan distance) or all goals.
  
## Main idea:
    The A* search algorithm is an informed search algorithm that uses a heuristic function to estimate the cost of reaching the goal from a given cell. It combines the cost of reaching a cell `g` and the estimated cost of reaching the goal from that cell `h` to determine the priority of exploring the cell. The algorithm uses a priority queue to keep track of the cells to be explored.

    For each cell, the algorithm explores all its neighbors and calculates the `g` and `h` values for each neighbor. If the neighbor is not blocked and has not been visited yet, the algorithm adds the neighbor to the priority queue. The algorithm continues until it finds a goal cell or the priority queue is empty.
    
    The algorithm can be used to find the shortest path to the seemingly nearest goal or all goals in the grid. If the agent can jump over obstacles, the algorithm will consider all valid neighbors of the current cell, and then choose the neighbor with the lowest `f` value (`g + h`) as the next cell.
"""
import heapq
from classes import *


def search(agent:Agent, all:bool=False) -> dict[str, list[str] | Cell | int] | int:
    """
    Perform A* search (informed) to find the shortest path from the agent's location to the goal.

    ### Args:
        - agent (Agent): The agent object. Can or cannot jump over obstacles.
        - all (bool, optional): True to find the shortest path to all goals; False to find the shortest path to the seemingly nearest goal. Defaults to False.

    ### Returns:
        - If a path is found:
            - dict: A dictionary to store the result of the search with the following keys:
                - 'path' (list[str]): A list of directions (up, left, down, right) to reach the goal.
                - 'goal' (Cell): The goal cell reached.
                - 'count' (int): The number of cells visited during the search.
        - If no path is found:
            - int: The number of cells visited during the search.
    """
    # tracemalloc.start()
    agent.grid.reset()
    start = agent.cell
    # If we only need one goal and the start cell is a goal, return an empty path immediately
    if not all and start in agent.goals:
        # tracemalloc.stop()
        return {
            'path': [],
            'goal': start,
            'count': 1
        }
    # Get the seemingly nearest goal based on Manhattan distance
    goal = min(agent.goals, key=start.manhattan_distance)
    # Initialize the h value for the start cell
    start.h = start.manhattan_distance(goal)

    # open_list = [start] # Use a list as a priority queue
    open_list:list[Cell] = [] # Use a heap as a priority queue
    heapq.heappush(open_list, start)
    closed_set = set()

    # Initialize the items of the result dictionary
    count = 1 # Start with 1 for the start cell
    path = []
    goals = set(agent.goals)
    reached_goals = []

    while open_list:
        # Get the cell with the lowest f value
        # current = min(open_list, key=lambda cell: cell.f)
        # open_list.remove(current)
        current = heapq.heappop(open_list)
        closed_set.add(current)

        if current in goals:
            reached_goals.append(current)
            goals.remove(current)
            path.extend(agent.trace_path(current))
            
            # If we only need one goal or all goals are reached, return the result immediately
            if not all or not goals:
                # tracemalloc.stop()
                return {
                    'path': path,
                    'goal': reached_goals if all else current,
                    'count': count
                }

            # Reset the search state for the next goal
            current.reset()
            for cell in closed_set:
                cell.reset()
            for cell in open_list:
                cell.reset()
            open_list = []
            heapq.heappush(open_list, current)
            closed_set = set()
            # Get the next nearest goal (seemingly)
            goal = min(goals, key=current.manhattan_distance)
            current.h = current.manhattan_distance(goal)
            # print("Next goal:", goal)
            continue

        for neighbor in agent.grid.get_neighbors(current, agent.can_jump):
            if neighbor in closed_set:
                continue

            tentative_g = current.g + current.jump_cost(neighbor)
            if neighbor not in open_list:
                # Increment the counter for each visited cell
                count += 1
                # Update the g and h values for the neighbor cell
                neighbor.g = tentative_g
                neighbor.h = neighbor.manhattan_distance(goal)
                # Set the parent of the neighbor cell to the current cell
                neighbor.parent = current
                # Add the neighbor to the open list
                # open_list.append(neighbor)
                heapq.heappush(open_list, neighbor)
            elif tentative_g < neighbor.g:
                # Update the neighbor's g value
                neighbor.g = tentative_g
                neighbor.parent = current
                # Reheapify the open list after updating the g value
                heapq.heapify(open_list)
    # If some goals are reached, return the result
    if reached_goals:
        return {
            'path': path,
            'goal': f"{reached_goals} (not all)",
            'count': count
        }
    # If no path is found, return the count of visited cells
    return count
