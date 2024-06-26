# COS30019 Assignment 1 - Tree Based Search for Robot Navigation Problem

## Introduction

  This is the source code for the Assignment 1 of course unit COS30019 - Introduction to Artificial Intelligence. Written in Python (3.12.0), the program implements tree-based search algorithms to search for solutions to the Robot Navigation problem, with both informed and uninformed methods.

### General Information

* Programming language: Python 3.12.0
* The program is designed to be executed with a CLI (e.g. Powershell for Windows).
* The original objective is to reach one of the green cells. However, the program has an option to find a path for **all** goals.
* The agent is aware of all features of the environment (goal locations, walls...). It can move in **four** directions: UP, LEFT, DOWN and RIGHT.
* The agent has an optional ability to jump over obstacles, with the jump cost increasing exponentially with the distance.

### Implemented Search Algorithms

* Uninformed
  * Breadth-First Search (BFS)
  * Depth-First Search (DFS)
  * Iterative Deepening Depth-First Search (IDDFS)
* Informed search algorithms:
  * A* Search (AStar)
  * Greedy Best-First Search (GBFS)
  * Bidirectional A* Search (BASS)

## Installation and Running

1. Make sure you have Python 3 installed.
2. Clone this repository to your local machine.
3. For searches, there is no need to install external packages. Navigate to the root folder and run the `search.py` file with CLI:

   * Unix/MacOS:

     ```
     python3 search.py <filename> <algorithm> [option]*
     ```
   * Windows:

     ```
     python search.py <filename> <algorithm> [option]*
     ```

   Replace `<filename>` with a filename in the ***maps/*** folder (not including the folder itself), and `<algorithm>` with an algorithm name. You can also provide additional options (`[option]*`) for different kinds of search (to find all goals, or to allow the agent to jump over walls...). Specific allowed algorithm names and options are listed at the end of the instruction.

   For example, for BFS search for **all** goals in map file *RobotNav-test.txt* on Windows:

   ```
   python search.py RobotNav-test.txt bfs -a
   ```

   Output follows the standard stated in the assignment instruction.
4. To use new map files, simply add the *.txt* file to the ***maps/*** folder. Map files are assumed to contain valid configurations in correct format as following:

   * First line contains a pair of numbers `[N,M]` – the number of rows and the number of columns of the grid, enclosed in square brackets.
   * Second line contains a pair of numbers `(x1,y1)` – the coordinates of the current location of the agent, the initial state.
   * Third line contains a sequence of pairs of numbers separated by `|`; these are the coordinates of the goal states: `(xG1,yG1) | (xG2,yG2) | … | (xGn,yGn)`, where `n ≥ 1`. That is, the goal states may have just one goal state, or two goal states, or many goal states.
   * The subsequent lines represent the locations of the walls: The tuple `(x,y,w,h)` indicates that the leftmost top corner of the wall occupies cell `(x,y)` with a width of `w` cells and a height of `h` cells.
5. For help and more information, run the command:

   ```
   python search.py help
   ```

   It will show lists of names for available search algorithms, map files, and allowed options.

### Algorithm names

* `bfs` for BFS
* `dfs` for DFS
* `iddfs` for IDDFS
* `gbfs` for GBFS
* `astar` for A* Search
* `bass` for Bidirectional A* Search

### Command options

* `-a`: Search for all goals
* `-j`: Agent can jump over obstacles i.e. walls
* `-l <number>`: Limit of visited cells for IDDFS, with `<number>` being a non-negative number (or you can specify this when prompted afterwards)


## Algorithm Performance Evaluation

  The `analyze.py` file in the root folder provides a simple tool to evaluate and analyze the performance of the algorithms in terms of result accuracy, efficiency, memory usage, and computation time, utilizing Python packages like timeit and tracemalloc. To run the script, use the command:

  ```
  python analyze.py [<filename> <algorithm>] [-n <number>] [-l <limit>]
  ```

  ### Arguments (All optional):
  
  * `<filename>`: a map filename in the ***maps/*** folder (default is *RobotNav-test.txt* if left empty).
  * `<algorithm>`: an algorithm name, as listed above (default is "bfs" if left empty).
  * `<number>`: the number of times each search should be executed to measure the average computation time from (default is 1000).
  * `<limit>`: the limit for the IDDFS algorithm, set to 0 if don't want limit (default is 1,000,000).

  ### Output:
  
  The chosen algorithm will perform searches in 4 different scenarios, combining these 2 features:
    * Whether the algorithm is searching for **all** goal or not.
    * Whether the agent can jump over obstacles or not.

  For each scenario, the search will be performed for the specified number of times, and the results for each scenario will be returned in the following format:
  ```
  Information:
    - Algorithm name
    - Map filename
    - Specific scenario
  Result:
    - Goals reached and path cost, or no goal reached
    - Count of explored nodes
  Performance:
    - Memory used in bytes
    - Average computation time in milliseconds
  ```
