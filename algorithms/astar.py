"""
A* Search Algorithm (informed)

## Functions:
    - search(agent:'Agent', all:bool=False) -> dict[list[str], 'Cell', int] | int: Perform A* search to find the shortest path from the agent's location to the seemingly nearest goal (estimated based on Manhattan distance) or all goals.
  
## Main idea:
    The A* search algorithm is an informed search algorithm that uses a heuristic function to estimate the cost of reaching the goal from a given cell. It combines the cost of reaching a cell `g` and the estimated cost of reaching the goal from that cell `h` to determine the priority of exploring the cell. The algorithm uses a priority queue to keep track of the cells to be explored.

    For each cell, the algorithm explores all its neighbors and calculates the `g` and `h` values for each neighbor. If the neighbor is not blocked and has not been visited yet, the algorithm adds the neighbor to the priority queue. The algorithm continues until it finds a goal cell or the priority queue is empty.
    
    The algorithm can be used to find the shortest path to the seemingly nearest goal or all goals in the grid. If the agent can jump over obstacles, the algorithm will consider all valid neighbors of the current cell, and then choose the neighbor with the lowest `f` value (`g + h`) as the next cell.
"""
import heapq, tracemalloc


def search(agent:'Agent', all:bool=False) -> dict[list[str], 'Cell', int] | int:
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
    open_list:list['Cell'] = [] # Use a heap as a priority queue
    heapq.heappush(open_list, start)
    closed_set = set()

    # Initialize the items of the result dictionary
    count = 1 # Start with 1 for the start cell
    path = []
    goals = set(agent.goals)
    reached_goals = []
    inner_count = 0

    while open_list:
        # Get the cell with the lowest f value
        # current = min(open_list, key=lambda cell: cell.f)
        # open_list.remove(current)
        current = heapq.heappop(open_list)
        closed_set.add(current)
        # if False and all and agent.can_jump and count > 17500:
        #     print("Updating current cell...")
        #     print(f"Count: {count}, Inner Count: {inner_count}, Open List ({len(open_list)}), Closed Set ({len(closed_set)}), Current: {current} - g: {current.g}, h: {current.h}, Parent: {current.parent}")
        #     print("Memory:", tracemalloc.get_traced_memory())
            
            # print("Resetting the inner count to 0...\n")
        inner_count = 0
        # if agent.can_jump:
        #     print(f"Open List: {open_list} - Current: {current} - Parent: {current.parent}")

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

        # neighbors = agent.grid.get_neighbors(current, agent.can_jump)
        # print(f"Current: {current} - g: {current.g}, h: {current.h}, Parent: {current.parent}, Neighbors: {", ".join([f"{neighbor} (g: {neighbor.g}, h: {neighbor.h})" for neighbor in neighbors])}")
        for neighbor in agent.grid.get_neighbors(current, agent.can_jump):
            inner_count += 1
            if neighbor in closed_set:
                continue
            # if all and agent.can_jump and count % 1000 == 0:
            #     print(f"Visited {count} cells")

            tentative_g = current.g + current.jump_cost(neighbor)
            if neighbor not in open_list:
                # print("Current:", current, "Neighbor:", neighbor)
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
                # print(f"Current: {current}, Neighbor: {neighbor} (Parent: {neighbor.parent}), Tentative g: {tentative_g}, Neighbor g: {neighbor.g}, Count: {count}")
                neighbor.g = tentative_g
                neighbor.parent = current
                # Reheapify the open list after updating the g value
                heapq.heapify(open_list)
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
    # maps.append("map.txt")
    # maps.append("map_7.txt")
    # maps.append("map_9.txt")
    maps = get_available_maps()
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
    