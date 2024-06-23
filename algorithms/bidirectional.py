"""
Bidirectional search algorithm (informed)

## Functions:
    - connect(agent: 'Agent', start: 'Cell', goal: 'Cell') -> None: Connect the path from the start cell to the goal cell.
    - search(agent: 'Agent') -> dict[list[str], 'Cell', int] | int: Perform bidirectional A* search to find the shortest path from the agent's location to the (seemingly) nearest goal.
  
## Main idea:
    The bidirectional A* search algorithm is an informed search algorithm that explores the search space from both the start and goal cells simultaneously. It uses two open lists to keep track of the cells to be explored from the start and goal cells. The algorithm continues until it finds a common cell in both open lists or one of the open lists is empty.

    For each cell, the algorithm explores all its neighbors (in the order of up, left, down, right) and adds them to the open list if they are not blocked and have not been visited yet. The algorithm continues until it finds a common cell in both open lists or one of the open lists is empty.
"""
import heapq


def connect(agent:'Agent', start:'Cell', goal:'Cell'):
    """
    Connect the path from the start cell to the goal cell. This is dedicated to find the best path from a cell to its neighbor when the agent can jump, instead of just jumping regardless of cost.
    
    Bidirectional A* Search Algorithm checks for a collapse of the two open lists when iterating each of their neighbors instead of checking the current cells. This can be a problem when the agent can jump, as the agent may jump from a cell straight to its neighbor when it finds collapse with distance greater than 1 instead of choosing the cell with smallest `f` value as in A*. This function is used to connect the path from the current cell to that possibly far neighbor cell, ensuring that the agent takes the best path by setting appropriate parent cells.

    ### Args:
        - agent (Agent): The agent object. Should be able to jump.
        - start (Cell): The start cell.
        - goal (Cell): The goal cell, which is actually a neighbor.

    ### Returns:
        None
    """
    if agent.can_jump:
        direction = goal - start
        neighbors:list['Cell'] = []
        neighbor = agent.grid.get_neighbor(start, direction)
        while neighbor is not None and neighbor != goal:
            if not neighbor.blocked:
                neighbor.g = start.g + start.jump_cost(neighbor)
                neighbor.h = neighbor.manhattan_distance(goal)
                neighbors.append(neighbor)
            neighbor = agent.grid.get_neighbor(neighbor, direction)
        # print(f"{start} => {goal} ({direction}) - Neighbors: {neighbors}")
        current = None
        while neighbors:
            current = min(neighbors, key=lambda cell: (cell.f, cell.h))
            current.parent = start
            start = current
            neighbors = neighbors[neighbors.index(current)+1:]
            for neighbor in neighbors:
                neighbor.g = start.g + start.jump_cost(neighbor)
                neighbor.h = neighbor.manhattan_distance(goal)
    goal.parent = start


def search(agent:'Agent', all:bool=False) -> dict[list[str], 'Cell', int] | int:
    """
    Perform bidirectional A* search to find the shortest path from the agent's location to the goal.

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
    # Get the seemingly nearest goal based on Manhattan distance
    goal = min(agent.goals, key=start.manhattan_distance)
    # Initialize the h value for the start cell
    start.h = goal.h = start.manhattan_distance(goal)

    # Use a list as a priority
    # open_list_start = [start]queue
    # open_list_goal = [goal]

    # Use a heap as a priority queue
    open_list_start:list['Cell'] = []
    heapq.heappush(open_list_start, start)
    open_list_goal:list['Cell'] = []
    heapq.heappush(open_list_goal, goal)

    closed_set_start = set()
    closed_set_goal = set()

    # Initialize the counter of the result dictionary
    count = 1  # Start with 1 for the start cell
    path = []
    goals = set(agent.goals)
    reached_goals = []

    while open_list_start and open_list_goal:
        # Update the current start and goal cells
        # current_start = min(open_list_start, key=lambda cell: cell.f)
        # open_list_start.remove(current_start)
        # current_goal = min(open_list_goal, key=lambda cell: cell.f)
        # open_list_goal.remove(current_goal)
        current_start = heapq.heappop(open_list_start)
        current_goal = heapq.heappop(open_list_goal)
        closed_set_start.add(current_start)
        closed_set_goal.add(current_goal)
        
        found_goal = False

        # print(f"Open List Start: {open_list_start} - Open List Goal: {open_list_goal}")
        # print(f"Current Start: {current_start} <= {current_start.parent} - Current Goal: {current_goal} <= {current_goal.parent}")

        # Explore the neighbors of the current start
        for neighbor in agent.grid.get_neighbors(current_start, agent.can_jump):
            if neighbor in closed_set_start:
                continue

            tentative_g = current_start.g + current_start.jump_cost(neighbor)
            if neighbor not in open_list_start:
                count += 1
                if neighbor.parent:  # If the neighbor has a parent, a path is found
                    # print("Tracing path from current start:", current_start, "to", neighbor)
                    found_goal = True
                    start.parent = goal.parent = None
                    # Extend the path
                    connect(agent, neighbor.parent, neighbor)
                    path_goal = agent.trace_path(neighbor, backward=False)
                    # neighbor.parent = current_start
                    connect(agent, current_start, neighbor)
                    path_start = agent.trace_path(neighbor)
                    path.extend(path_start + path_goal)
                    break
                # Update the g and h values, and parent for the neighbor cell
                neighbor.g = tentative_g
                neighbor.h = neighbor.manhattan_distance(goal)
                neighbor.parent = current_start
                # Add the neighbor to the open list
                # open_list_start.append(neighbor)
                heapq.heappush(open_list_start, neighbor)
            elif tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.parent = current_start
                # Reheapify the open list after updating the g value
                heapq.heapify(open_list_start)

        for neighbor in agent.grid.get_neighbors(current_goal, agent.can_jump):
            if neighbor in closed_set_goal:
                continue

            tentative_g = current_goal.g + current_goal.jump_cost(neighbor)
            if neighbor not in open_list_goal:
                count += 1
                if neighbor.parent and not found_goal:
                    # print("Tracing path from current goal:", current_goal, "to", neighbor)
                    found_goal = True
                    start.parent = goal.parent = None
                    # Extend the path
                    connect(agent, neighbor.parent, neighbor)
                    path_start = agent.trace_path(neighbor)
                    # neighbor.parent = current_goal
                    connect(agent, current_goal, neighbor)
                    path_goal = agent.trace_path(neighbor, backward=False)
                    path.extend(path_start + path_goal)
                    break
                neighbor.g = tentative_g
                neighbor.h = neighbor.manhattan_distance(start)
                neighbor.parent = current_goal
                # open_list_goal.append(neighbor)
                heapq.heappush(open_list_goal, neighbor)
            elif tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.parent = current_goal
                heapq.heapify(open_list_goal)
        # If a goal is found, reset the search state for the next goal
        if found_goal:
            reached_goals.append(goal)
            goals.remove(goal)
            if not all or not goals:
                return {
                    'path': path,
                    'goal': reached_goals if all else goal,
                    'count': count
                }
            agent.grid.reset()
            start = goal
            goal = min(goals, key=start.manhattan_distance)
            start.h = goal.h = start.manhattan_distance(goal)

            open_list_start = []
            heapq.heappush(open_list_start, start)
            closed_set_start = set()

            open_list_goal = []
            heapq.heappush(open_list_goal, goal)
            closed_set_goal = set()
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
    setup_3 = """
agent.can_jump = True
    """
    
    import sys, os, timeit

    directory = os.path.dirname(os.path.dirname(__file__))
    sys.path.append(directory)

    from classes import *
    from utils import *

    maps = []
    # maps.append("map_5.txt")
    # maps.append("map_7.txt")
    # maps.append("map_8.txt")
    maps.append("map_9.txt")
    # maps = get_available_maps()
    for file in maps:
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
        
        # result = search_all(agent)
        # print("Search All (Old):", result)
        
        result = search(agent, all=True)
        print("Search All:", result)
        print(f"Time: {timeit.timeit("search(agent, all=True)", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)\nPath Length: {len(result['path']) if type(result) == dict else 0}\n")
        
        print("Enabled Jumping\n")
        agent.can_jump = True
        result = search(agent)
        print("Search:", result)
        print(f"Time: {timeit.timeit("search(agent)", setup=setup+setup_2+setup_3, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        
        result = search(agent, all=True)
        print("Search All:", result)
        print(f"Time: {timeit.timeit("search(agent, all=True)", setup=setup+setup_2+setup_3, number=number)*1000/number} milliseconds (average of {number} runs)\n")
        # break