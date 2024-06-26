"""
Iterative Deepening Depth-First Search (IDDFS) Algorithm (uninformed)
  
## Functions:
    - dls(agent:Agent, current:Cell, depth:int, visited:set, count:int, limit:int) -> dict[str, bool | int | Cell]: Perform depth-limited search to find the shortest path from the current cell to the target cell.
    - search(agent:Agent, all:bool=False limit: int=10**6) -> dict[str, list[str] | Cell | int] | int: Perform iterative deepening depth-first search to find the shortest path from the agent's location to the nearest goal or all goals.

## Main idea:
    The iterative deepening depth-first search algorithm is an uninformed search algorithm that combines the benefits of depth-first search and breadth-first search. It performs depth-limited search with increasing depth limits until the goal is found. The algorithm continues until it finds a goal cell or the maximum depth is reached.
    
    For each cell, the algorithm explores all its neighbors in the order of up, left, down, right and adds them to the stack if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the maximum depth is reached.
    
    The algorithm also includes a limit parameter to stop the search if the number of visited cells exceeds the limit.
"""
import copy
from classes import *


def dls(agent:Agent, current:Cell, depth:int, visited:set, count:int, limit:int) -> dict[str, bool | int | Cell]:
    """
    Perform depth-limited search to find the shortest path from the current cell to the target cell.

    ### Args:
        - agent (Agent): The agent object. Can or cannot jump over obstacles.
        - current (Cell): The current cell.
        - depth (int): The current depth to explore.
        - visited (set): A set to store visited cells.
        - count (int): The number of cells visited during the search.
        - limit (int): The maximum number of cells to visit during the search before stopping.

    ### Returns:
        - dict: A dictionary to store the result of the search with the following keys:
            - 'success' (bool): True if the target cell is found; False otherwise.
            - 'count' (int): The number of cells visited during the search.
            - 'goal' (Cell, optional): The goal cell reached. If the target cell is not found, this key is not included.
    """
    if current in agent.goals:
        return {
            'success': True,
            'goal': current,
            'count': count
        }
    # If the maximum depth is reached, stop recursion
    if depth == 0:
        return {
            'success': False,
            'count': count
        }

    for neighbor in agent.grid.get_neighbors(current, agent.can_jump):
        # If the number of visited cells exceeds the limit, stop recursion and accept failure
        if limit > 0 and count >= limit:
            return {
                'success': False,
                'count': count
            }
        # Skip blocked cells
        if neighbor in visited:
            continue
        visited.add(neighbor)
        count += 1
        result = dls(agent, neighbor, depth - 1, visited, count, limit)
        count = result['count']
        if result['success']:
            neighbor.parent = current
            return {
                'success': True,
                'goal': result['goal'],
                'count': count
            }
        visited.remove(neighbor)
    # If the target cell is not found, return the count of visited cells
    return {
        'success': False,
        'count': count
    }


def search(agent:Agent, all:bool=False, limit:int=10**6) -> dict[str, list[str] | Cell | int] | int:
    """
    Perform iterative deepening depth-first search to find the shortest path from the agent's location to a goal.

    ### Args:
        - agent (Agent): The agent object. Can or cannot jump over obstacles.
        - all (bool, optional): True to find the shortest path to all goals; False to find the shortest path to one goal. Default is False.
        - limit (int, optional): The maximum number of cells to visit during the search before stopping. Set to 0 to disable this. Default is 1,000,000.

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
        
    max_depth = agent.grid.net_area
    
    # Initialize the items of the result dictionary
    count = 1  # Start with 1 for the start cell
    path = []
    goals = copy.deepcopy(agent.goals)
    reached_goals = []

    while agent.goals and (count < limit or limit == 0):
        found_goal = False
        for depth in range(1, max_depth + 1):
            # Initialize a set to store visited cells for each depth
            visited = {start}
            result = dls(agent, start, depth, visited, count, limit)
            count = result['count']
            if result['success']:
                goal = result['goal']
                reached_goals.append(goal)
                agent.goals.remove(goal)
                path.extend(agent.trace_path(goal))
                # If we only need one goal or all goals are reached, return the result immediately
                if not all or not agent.goals:
                    agent.goals = goals
                    return {
                        'path': path,
                        'goal': goals if all else goal,
                        'count': count
                    }
                # Reset the search state for the next goal
                start = goal
                start.reset()
                found_goal = True
                break
            if count >= limit and limit > 0:
                break
        # If there is no path to any goals, stop the search
        if not found_goal:
            break
    # Reset the goals of the agent
    agent.goals = goals
    # If some goals are reached, return the result
    if reached_goals:
        return {
            'path': path,
            'goal': f"{reached_goals} (not all)",
            'count': count
        }
    # If no path is found, return the count of visited cells
    return count
