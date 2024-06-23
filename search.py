import sys
# Functions to handle map files
from utils import *
# Classes of the environment
from classes import *
# Function to import needed search algorithm
from importlib import import_module

ALLOWED_TAGS = {
    "-a": "Search all goals",
    "-j": "Jump point search",
    "-l": "Limit of visited cells for IDDFS (or you can specify this when prompted afterwards)"
}

# Get system arguments
args = sys.argv
# args = ["search.py", "RobotNav-test.txt", "astar"]
# # args += ["-a"]
# # args += ["-j"]
# args += ["-l", "10000"]

# Process the system arguments
try:
    # Get the map file name and search algorithm
    filename = args[1]

    if filename == "help":
        print("\nTree Based Search for Robot Navigation Problem - CLI Help\n")

        print("Available search algorithms:")
        for alg in get_available_algorithms():
            print("\t-", alg)

        print("\nAvailable map files:")
        for file in get_available_maps():
            print("\t-", file)

        print("\nTags:")
        for tag, desc in ALLOWED_TAGS.items():
            print(f"\t{tag}: {desc}")

        print(
            "\nCommand Format: 'python search.py <filename> <algorithm> [tags]'")
        print("Example:\
      \n\t'python search.py RobotNav-test.txt dfs',\
      \n\t'python search.py .\\map_2.txt iddfs -l 10000',\
      \n\t'python search.py no_goal.txt bfs -a -j'")

        print()
        sys.exit()

    algorithm_name = args[2].lower()

    # Load the map and create the agent
    size, agent_loc, goal_locs, walls = load_map(filename)
    map = Grid(size, walls)
    agent = Agent(map, agent_loc, goal_locs, can_jump="-j" in args)

    # Import the desired search algorithm from the algorithms package
    algorithm = import_module(name="algorithms." + algorithm_name)

    # search_type = "search_jps" if "-j" in args else search_type
    limit = 0

    # If the search algorithm is IDDFS, get the limit of visited cells
    if algorithm.__name__ == "algorithms.iddfs":
        if "-l" in args:
            limit = int(args[args.index("-l") + 1])
        else:
            limit_str = input(
                "Enter the limit of number of visited cells (Default 100,000): ").strip()
            if limit_str != "" and type(eval(limit_str)) == int:
                limit = int(limit_str)
            else:
                limit = 10**5

    if limit != 0:
        result = algorithm.search(agent=agent, limit=limit, all="-a" in args)
    else:
        result = algorithm.search(agent=agent, all="-a" in args)

    # Print the result of the search
    print(filename, algorithm_name)
    if type(result) == dict:  # A goal is found
        print(result['goal'], result['count'])
        print(result['path'])
    else:  # No goal is found
        print("No goal is reachable;", result)

# Handle exceptions
# In case of missing arguments
except IndexError:
    print("ERROR: Missing arguments.")
    print("Please provide the name of the map file and search algorithm using this command format: 'python search.py <filename> <algorithm_name>'")
    print("Example: 'python search.py RobotNav-test.txt dfs')")
    suggest_help()

# In case of inexistent map file
except FileNotFoundError:
    print("ERROR: Map file not found.")
    print("Available maps are:", get_available_maps())
    suggest_help()

# In case of invalid search algorithm
except ModuleNotFoundError:
    print("ERROR: Search algorithm not found.")
    print("Allowed algorithms are:", get_available_algorithms())
    suggest_help()
