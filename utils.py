"""
Handles the loading and printing of the map from a text file.

Functions:
    - load_map(file_name: str) -> Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]], List[Tuple[int, int, int, int]]]
    - print_map(grid_size: Tuple[int, int], agent_loc: Tuple[int, int], goal_locs: List[Tuple[int, int]], walls: List[Tuple[int, int, int, int]]) -> None
"""
import os
import psutil
# Function to list all modules in a package
from pkgutil import iter_modules

FILENAME = "RobotNav-test.txt"
FREE = '0'
AGENT = 'A'
GOAL = 'G'
WALL = '1'


def get_available_maps() -> list[str]:
    """
    Get the list of available map files in the "maps" folder.

    ### Returns:
        - list[str]: A list of map file names.
    """
    directory = os.path.dirname(__file__)
    map_dir = os.path.join(directory, "maps")
    return os.listdir(map_dir)


def get_available_algorithms() -> list[str]:
    """
    Get the list of available algorithm files in the "algorithms" folder.

    ### Returns:
        - list[str]: A list of algorithm file names.
    """
    directory = os.path.dirname(__file__)
    alg_dir = os.path.join(directory, "algorithms")
    modules = [name for _, name, _ in iter_modules([alg_dir])]
    return modules


def load_map(file_name:str=FILENAME) -> tuple[tuple[int,int], tuple[int,int], list[tuple[int,int]], list[tuple[int,int,int,int]]]:
    """
    Load the map from a text file.

    ### Args:
        - file_name (str, optional): The name of the text file containing the map. Defaults to FILENAME.

    ### Returns:
        - tuple[int, int]: grid size
        - tuple[int, int]: agent's initial location
        - list[tuple[int, int]]: goal locations
        - list[tuple[int, int, int, int]]: wall locations
    """
    dir_path = os.path.join(os.path.dirname(__file__), "maps")
    file_path = os.path.join(dir_path, file_name)
    with open(file_path) as f:
        grid_size = f.readline().strip()    # This is a list of grid dimensions
        grid_size = eval(grid_size)

        agent_loc = f.readline().strip()    # This is a tuple of agent's initial location
        agent_loc = eval(agent_loc)

        goal_locs = f.readline().strip().split(
            '|')    # This is a list of goal locations
        goal_locs = list(map(eval, goal_locs))

        walls = []                      # This is a list of wall locations
        wall = f.readline().strip()
        while wall:                    # Read until the end of the file
            walls.append(eval(wall))
            wall = f.readline().strip()

    return grid_size, agent_loc, goal_locs, walls


def print_map(grid_size:tuple[int,int], agent_loc:tuple[int,int], goal_locs:list[tuple[int,int]], walls:list[tuple[int,int,int,int]], end:str="\n"):
    """
    Print the map to the console.

    ### Args:
        - grid_size (tuple[int, int]): The dimensions of the grid.
        - agent_loc (tuple[int, int]): The agent's initial location.
        - goal_locs (list[tuple[int, int]]): A list of goal locations.
        - walls (list[tuple[int, int, int, int]]): A list of wall locations.
        - end (str, optional): The character to print at the end of the map. Defaults to "\\n".

    ### Returns:
        None
    """
    height, width = grid_size
    for y in range(height):
        for x in range(width):
            if (x, y) == agent_loc:
                print(AGENT, end="")
            elif (x, y) in goal_locs:
                print(GOAL, end="")
            else:
                is_wall = False
                for wall in walls:
                    if wall[0] <= x < wall[0] + wall[2] and wall[1] <= y < wall[1] + wall[3]:
                        print(WALL, end="")
                        is_wall = True
                        break
                if not is_wall:
                    print(FREE, end="")
        print()
    print(end, end="")


def suggest_help():
    """
    Suggest the user to use the help option of search.py.

    ### Returns:
        None
    """
    print("\nFor more information, use the help option: 'python search.py help'\n")


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


if __name__ == "__main__":
    result = grid_size, agent_loc, goal_locs, walls = load_map("map_8.txt")
    print_map(*result)
    print("Available maps:", get_available_maps())
    print("Available algorithms:", get_available_algorithms())
