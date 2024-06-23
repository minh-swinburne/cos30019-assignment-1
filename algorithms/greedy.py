"""
Greedy Best-First Search Algorithm (informed)

## Functions:
    - search(agent:'Agent', all:bool=False) -> dict[list[str], 'Cell', int] | int: Perform greedy search to find the (seemingly) shortest path from the agent's location to the (seemingly) nearest goal or all goals.
  
## Main idea:
    The greedy best-first search algorithm is an informed search algorithm that explores the search space based on the heuristic value of each cell, which is the Manhattan distance from the cell to a goal. It uses a priority queue to keep track of the cells to be explored.

    For each cell, the algorithm explores all its neighbors (in the order of up, left, down, right) and adds them to the priority queue if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the priority queue is empty.
    
    The algorithm can be used to find the seemingly shortest path to the seemingly nearest goal or all goals in the grid. If the agent can jump over obstacles, the algorithm will consider all valid neighbors of the current cell, and then choose the neighbor with lowest Manhattan distance to the current goal as the next cell, regardless of the cost to reach it.
"""
import heapq


def search(agent:'Agent', all:bool = False) -> dict[list[str], 'Cell', int] | int:
    """
    Perform greedy search (informed) to find the shortest path from the agent's location to the goal.

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
    agent.grid.reset()
    start = agent.cell
    # If we only need one goal and the start cell is a goal, return an empty path immediately
    if not all and start in agent.goals:
        return {
            'path': [],
            'goal': start,
            'count': 1
        }
    # Get the seemingly nearest goal based on Manhattan distance
    goal = min(agent.goals, key=start.manhattan_distance)
    start.h = start.manhattan_distance(goal)

    # open_list = [start]
    # Use a heap as a priority queue
    open_list:list[tuple[int, 'Cell']] = []
    # Push the start cell with its h value to the heap
    heapq.heappush(open_list, (start.h, start))
    closed_set = set()

    # Initialize the items of the result dictionary
    count = 1  # Start with 1 for the start cell
    path = []
    goals = set(agent.goals)
    reached_goals = []

    while open_list:
        # current = min(open_list, key=lambda cell: cell.h)
        # open_list.remove(current)
        # Pop the cell with the lowest h value (ignoring the h value)
        _, current = heapq.heappop(open_list)
        closed_set.add(current)

        if current in goals:
            reached_goals.append(current)
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
            # agent.grid.reset()
            # current.reset()
            for cell in closed_set:
                cell.reset()
            for _, cell in open_list:
                cell.reset()
            open_list = []
            heapq.heappush(open_list, (current.h, current))
            closed_set = set()
            # Get the next nearest goal (seemingly)
            goal = min(goals, key=current.manhattan_distance)
            current.h = current.manhattan_distance(goal)
            # print("Next goal:", goal)
            continue

        for neighbor in agent.grid.get_neighbors(current, agent.can_jump):
            if neighbor in closed_set:
                continue
            if neighbor not in [cell for _, cell in open_list]:
                # Increment the counter for each visited cell
                count += 1
                neighbor.h = neighbor.manhattan_distance(goal)
                neighbor.parent = current
                # open_list.append(neighbor)
                # Push the neighbor cell with its h value to the heap
                heapq.heappush(open_list, (neighbor.h, neighbor))
    # If no path is found, return the count of visited cells
    return count


if __name__ == "__main__":
    setup = """
import sys, os

directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(directory)

from classes import Cell, Grid, Agent
from utils import load_map
from __main__ import search
    """
    import sys, os, timeit

    directory = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(directory)

    from classes import *
    from utils import *

    for file in get_available_maps():
        print(file)
        grid_size, agent_loc, goal_locs, walls = load_map(file)
        map = Grid(grid_size, walls)
        agent = Agent(map, agent_loc, goal_locs)
        print_map(grid_size, agent_loc, goal_locs, walls)
        
        setup_2 = f"""
grid_size, agent_loc, goal_locs, walls = load_map('{file}')
grid_map = Grid(grid_size, walls)
agent = Agent(grid_map, agent_loc, goal_locs)
        """
        number = 10
        
        result = search(agent)
        print("Search:", result)
        print(f"Time: {timeit.timeit("search(agent)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        
        result = search(agent, all=True)
        print("Search All:", result)
        print(f"Time: {timeit.timeit("search(agent, all=True)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        
        print("Enabled Jumping\n")
        agent.can_jump = True
        result = search(agent)
        print("Search:", result)
        print(f"Time: {timeit.timeit("search(agent)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        result = search(agent, all=True)
        print("Search All:", result)
        print(f"Time: {timeit.timeit("search(agent, all=True)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        # break
