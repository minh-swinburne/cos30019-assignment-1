import sys, os, timeit, tracemalloc, psutil
from classes import *
from utils import *
from importlib import import_module

args = sys.argv

map_file = FILENAME
algorithm = "bfs"
all = False
can_jump = False

if len(args) > 1:
    map_file = args[1]
if len(args) > 2:
    algorithm = args[2]
if "-a" in args:
    all = True
if "-j" in args:
    can_jump = True

print(f"\nAnalyzing {algorithm.upper()} algorithm for map in file {map_file} ({"All goals" if all else "One goal"}, agent CAN{"NOT" if not can_jump else ""} jump)...")

# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

# decorator function
def profile(func):
    def wrapper(*args, **kwargs):

        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}:consumed memory: {:,}\n".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))

        return result
    return wrapper

# instantiation of decorator function
@profile
def analyze(map_file, algorithm, all, can_jump, number=1000):
    setup = f"""
import sys, os

directory = os.path.dirname(os.path.dirname(__file__))
sys.path.append(directory)

from classes import Cell, Grid, Agent
from utils import load_map
from importlib import import_module

algorithm = import_module(name="algorithms.{algorithm}")
    """
    # directory = os.path.dirname(os.path.dirname(__file__))
    # sys.path.append(directory)

    # algorithm = import_module(name=f"algorithms.{ALGORITHM}")

    # grid_size, agent_loc, goal_locs, walls = load_map(file)
    # map = Grid(grid_size, walls)
    # agent = Agent(map, agent_loc, goal_locs)
    # print_map(grid_size, agent_loc, goal_locs, walls)
    
    setup_2 = f"""
grid_size, agent_loc, goal_locs, walls = load_map('{map_file}')
grid_map = Grid(grid_size, walls)
agent = Agent(grid_map, agent_loc, goal_locs)
agent.can_jump = {can_jump}
    """
    
    # result = algorithm.search(agent)
    # print("Search:", result)
    print(f"Result:")
    tracemalloc.start()
    print(f"\t- Time: {timeit.timeit(f"algorithm.search(agent, all={all})", setup=setup+setup_2, number=number)*1000/number} milliseconds (average of {number} runs)")
    print(f"\t- Memory used: {tracemalloc.get_traced_memory()[1]}")
    tracemalloc.stop()
        
analyze(map_file, algorithm, all, can_jump, 1000)