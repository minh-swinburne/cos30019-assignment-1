"""
Breadth-First Search (BFS) Algorithm (uninformed)

## Functions:
    - search(agent:'Agent', all:bool=False) -> dict[list[str], 'Cell', int] | int: Perform breadth-first search to find the shortest path from the agent's location to the nearest goal or all goals.

## Main idea:
    The breadth-first search algorithm is an uninformed search algorithm that explores all the nodes at the present depth before moving on to the nodes at the next depth level. It uses a queue to keep track of the nodes to be explored.

    For each cell, the algorithm explores all its neighbors (in the order of up, left, down, right) and adds them to the queue if they are not blocked and have not been visited yet. The algorithm continues until it finds a goal cell or the queue is empty.

    The algorithm can be used to find the shortest path to the nearest goal or all goals in the grid. If the agent can jump over obstacles, the algorithm will consider all valid neighbors of the current cell, regardless of their costs.
"""
from collections import deque


def search(agent:'Agent', all:bool=False) -> dict[list[str], 'Cell', int] | int:
    """
    Perform breadth-first search to find the shortest path from the agent's location to the nearest goal or all goals.

    ### Args:
        - agent (Agent): The agent object. Can or cannot jump over obstacles.
        - all (bool, optional): True to find the shortest path to all goals; False to find the shortest path to the nearest goal. Defaults to False.

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
    # queue = [start]
    queue = deque([start])
    visited = {start}

    # Initialize the items of the result dictionary
    count = 1 # Start with 1 for the start cell
    path = []
    goals = set(agent.goals)
    reached_goals = []

    while queue:
        # Pop the first cell from the queue
        # current = queue.pop(0)
        current = queue.popleft()
        # If the current cell is a goal
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
            # queue = [current]
            queue = deque([current])
            visited = {current}
            current.parent = None
            continue

        # Explore all valid neighbors of the current cell, regardless of their costs
        for neighbor in agent.grid.get_neighbors(current, agent.can_jump):
            if neighbor not in visited:
                # Increment the counter for each visited cell
                count += 1
                # Append the neighbor to the end of the queue (FIFO)
                queue.append(neighbor)
                visited.add(neighbor)
                neighbor.parent = current
    # If no path is found, return the count of visited cells
    return count


# Test the algorithm
if __name__ == "__main__":
    setup = """
import sys, os

directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(directory)

from classes import Cell, Grid, Agent
from utils import load_map
from __main__ import search
    """
    setup_3 = """
agent.can_jump = True
    """
    
    import sys, os, timeit

    directory = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(directory)

    from classes import *
    from utils import *
    
    @profile
    def run_search(agent:Agent, all=False, number=100):        
        result = search(agent, all=all)
        print(f"Search{" All" if all else ""}{" (jump)" if agent.can_jump else ""}:", result)
        print(f"Time: {timeit.timeit("search(agent, all={all})", setup=setup+setup_2+(setup_3 if agent.can_jump else """"""), number=number)*1000/number} milliseconds (average of {number} runs)")
        
    for file in get_available_maps():
        print(file)
        grid_size, agent_loc, goal_locs, walls = load_map(file)
        map = Grid(grid_size, walls)
        print(map.net_area)
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
        print(f"Time: {timeit.timeit("search(agent)", setup=setup+setup_2+setup_3, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        
        result = search(agent, all=True)
        print("Search All:", result)
        print(f"Time: {timeit.timeit("search(agent, all=True)", setup=setup+setup_2+setup_3, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        
        # run_search(agent)        
        # run_search(agent, True)
        
        # print("Enabled Jumping\n")
        # agent.can_jump = True
        
        # run_search(agent)        
        # run_search(agent, True)
        # break
