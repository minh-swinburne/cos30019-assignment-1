import sys, timeit, tracemalloc
from classes import *
from utils import *
from importlib import import_module


def space(agent, algorithm, all, limit):
    tracemalloc.reset_peak()
    tracemalloc.clear_traces()
    tracemalloc.start()
    if algorithm.__name__ == "algorithms.iddfs":
        result = algorithm.search(agent, all=all, limit=limit)
    else:
        result = algorithm.search(agent, all=all)
    memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return result, memory[1]


def time(map_file, algorithm_str, all, can_jump, limit, number=1000):
    setup = f"""
import sys, os

directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(directory)

from classes import Cell, Grid, Agent
from utils import load_map
from importlib import import_module

algorithm = import_module(name="algorithms.{algorithm_str}")
grid_size, agent_loc, goal_locs, walls = load_map('{map_file}')
grid_map = Grid(grid_size, walls)
agent = Agent(grid_map, agent_loc, goal_locs)
agent.can_jump = {can_jump}
    """
    stmt = f"algorithm.search(agent, all={all}"
    if algorithm_str == "iddfs":
        stmt += f", limit={limit}"
    stmt += ")"
    
    return timeit.timeit(stmt, setup=setup, number=number)*1000/number


def analyze(map_file, algorithm_str, all, can_jump, limit, number):    
    print("Information:")
    print("\t- Algorithm:", algorithm_str.upper())
    print("\t- Map:", map_file)
    print(f"\t- {"All goals" if all else "One goal"}, agent CAN{'NOT' if not can_jump else ''} jump")
    
    grid_size, agent_loc, goal_locs, walls = load_map(map_file)
    
    if goal_locs:
        grid_map = Grid(grid_size, walls)
        agent = Agent(grid_map, agent_loc, goal_locs)
        agent.can_jump = can_jump
        algorithm = import_module(name=f"algorithms.{algorithm_str}")

        result, peak_memory = space(agent, algorithm, all, limit)
    else:
        result = 0
        peak_memory = 0
    
    print("Result:")
    if type(result) == dict:
        print(f"\t- Goal(s): {result['goal']}")
        goal, cost = agent.traverse_path(result['path'])
        print(f"\t- Cells visited: {result['count']:,}")
        print(f"\t- Path Cost: {cost:,} => Final Goal: {goal}")
    else:
        print(f"\t- No goal reached; cells visited: {result:,}")
        
    print("Performance:")
    print(f"\t- Memory used: {peak_memory:,} B")
    avg_time = time(map_file, algorithm_str, all, can_jump, limit, number)
    print(f"\t- Time: {avg_time:,.4f} milliseconds (average of {number} runs)")
    print()


args = sys.argv

map_file = FILENAME
algorithm_str = "bfs"
number = 1000
limit = 10**6

if len(args) > 1:
    map_file = args[1]
if len(args) > 2:
    algorithm_str = args[2]
if "-n" in args:
    index = args.index("-n")
    number = int(args[index+1])
if "-l" in args:
    index = args.index("-l")
    limit = int(args[index+1])

# analyze(map_file, algorithm_str, all, can_jump, limit, number)
# for algorithm_str in get_available_algorithms():
analyze(map_file, algorithm_str, False, False, limit, number)
analyze(map_file, algorithm_str, True, False, limit, number)
analyze(map_file, algorithm_str, False, True, limit, number)
analyze(map_file, algorithm_str, True, True, limit, number)
