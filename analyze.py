import sys, timeit, tracemalloc
from classes import *
from utils import *
from importlib import import_module


def space(agent, algorithm, all):
    tracemalloc.reset_peak()
    tracemalloc.clear_traces()
    tracemalloc.start()
    result = algorithm.search(agent, all=all)
    memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return result, memory[1]


def time(map_file, algorithm_str, all, can_jump, number=1000):
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
    
    return timeit.timeit(f"algorithm.search(agent, all={all})", setup=setup, number=number)*1000/number


def analyze(map_file, algorithm_str, all, can_jump, number):    
    print("\nInformation:")
    print("\t- Algorithm:", algorithm_str.upper())
    print("\t- Map:", map_file)
    print("\t- All goals" if all else "One goal", f", agent CAN{'NOT' if not can_jump else ''} jump")
    
    grid_size, agent_loc, goal_locs, walls = load_map(map_file)
    grid_map = Grid(grid_size, walls)
    agent = Agent(grid_map, agent_loc, goal_locs)
    agent.can_jump = can_jump
    algorithm = import_module(name=f"algorithms.{algorithm_str}")

    result, peak_memory = space(agent, algorithm, all)
    
    print("\nResult:")
    if type(result) == dict:
        print(f"\t- Goal(s): {result['goal']}")
        print(f"\t- Path Length: {len(result['path'])} => Final Goal: {agent.traverse_path(result['path'])}")
        print(f"\t- Cells visited: {result['count']}")
    else:
        print(f"\t- No goal reached; cells visited: {result}")
        
    print("\nPerformance:")
    print(f"\t- Memory used: {peak_memory:,} B")
    avg_time = time(map_file, algorithm_str, all, can_jump, number)
    print(f"\t- Time: {avg_time:.4f} milliseconds (average of {number} runs)")


args = sys.argv

map_file = FILENAME
algorithm_str = "bfs"
all = False
can_jump = False
number = 100

if len(args) > 1:
    map_file = args[1]
if len(args) > 2:
    algorithm_str = args[2]
if "-a" in args:
    all = True
if "-j" in args:
    can_jump = True
if "-n" in args:
    index = args.index("-n")
    number = int(args[index+1])

analyze(map_file, algorithm_str, all, can_jump, number)
