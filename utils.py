"""
Handles the loading and printing of the map from a text file.

Functions:
    - load_map(file_name: str) -> Tuple[Tuple[int, int], Tuple[int, int], List[Tuple[int, int]], List[Tuple[int, int, int, int]]]
    - print_map(grid_size: Tuple[int, int], agent_loc: Tuple[int, int], goal_locs: List[Tuple[int, int]], walls: List[Tuple[int, int, int, int]]) -> None
"""
import os, random
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


def suggest_help():
    """
    Suggest the user to use the help option of search.py.

    ### Returns:
        None
    """
    print("\nFor more information, use the help option: 'python search.py help'\n")


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

        goal_locs = f.readline().strip()    # This is a list of goal locations
        if goal_locs:
            goal_locs = list(map(eval, goal_locs.split('|')))
        else:
            goal_locs = []

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


def generate_map(rows, cols, start, goals, walls, filename):
    """
    Generate a map and save it to a text file.

    ### Args:
        - rows (int): The number of rows in the grid.
        - cols (int): The number of columns in the grid.
        - start (tuple[int, int]): The agent's initial location.
        - goals (list[tuple[int, int]]): A list of goal locations.
        - walls (list[tuple[int, int, int, int]]): A list of wall locations.
        - filename (str): The name of the text file to save the map.
        
    ### Returns:
        None
    """
    map_str = f"[{rows},{cols}]\n"
    map_str += f"({start[0]},{start[1]})\n"
    goals_str = " | ".join([f"({goal[0]},{goal[1]})" for goal in goals])
    map_str += f"{goals_str}\n"
    for wall in walls:
        map_str += f"({wall[0]},{wall[1]},{wall[2]},{wall[3]})\n"
    
    with open(os.path.join("maps", filename), "w") as f:
        f.write(map_str)


if __name__ == "__main__":
    # print("Available maps:", get_available_maps())
    # print("Available algorithms:", get_available_algorithms())
    
    # filename = "map_18.txt"
    filename = "no_goal_2.txt"
    height = 100
    width = 150
    start = (0, 0)
    goals = [(width-1, height-1), (width*3//4, height//5)]
    walls = []
    for _ in range(height*width//5):
        while True:
            direction = random.choice(["horizontal", "vertical"])
            cols = random.randint(1, 5) if direction == "horizontal" else 1
            rows = random.randint(1, 5) if direction == "vertical" else 1
            wall = (random.randint(0, width-cols), random.randint(0, height-rows), cols, rows)
            collapsed = False
            if wall[0] <= start[0] < wall[0] + wall[2] and wall[1] <= start[1] < wall[1] + wall[3]:
                collapsed = True
            for goal in goals:
                if wall[0] <= goal[0] < wall[0] + wall[2] and wall[1] <= goal[1] < wall[1] + wall[3]:
                    collapsed = True
            if not collapsed:
                walls.append(wall)
                break
    
    # generate_map(height, width, start, goals, walls, filename)
    result = grid_size, agent_loc, goal_locs, walls = load_map(filename)
    # result = grid_size, agent_loc, goal_locs, walls = load_map("map_10.txt")
    print(filename)
    print_map(*result)
