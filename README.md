# COS30019 Assignment 1 * Tree Based Search for Robot Navigation Problem

## Introduction

  This is the source code for the Assignment 1 of course unit COS30019 - Introduction to Artificial Intelligence. Written in Python (3.12.0), the program implements tree-based search algorithms to search for solutions to the Robot Navigation problem, with both informed and uninformed methods.

### General Information

  * Programming language: Python 3.12.0
  * The original objective is to reach one of the green cells.
  * The program has an option to find path for ALL goals.
  * The agent has an optional ability to jump over obstacles.
  * The program is designed to be executed with a CLI (e.g. Powershell for Windows).

### Implemented Search Algorithms

  * Uninformed
    * Breadth-First Search (BFS)
    * Depth-First Search (DFS)
    * Iterative Deepening Depth-First Search (IDDFS)
  * Informed search algorithms:
    * A* Search
    * Greedy Best-First Search (GBFS)
    * Bidirectional A* Search

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

     Replace `<filename>` with a filename in the ***maps/*** folder, and `<algorithm>` with an algorithm name. You can also provide additional options (`[option]*`) for different kinds of search (to find all goals, or to allow the agent to jump over walls...). Specific allowed algorithm names and options are listed at the end of the instruction.

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
  * `greedy` for GBFS
  * `astar` for A* Search
  * `bi_astar` for Bidirectional A* Search

### Command options

  * `-a`: Search for all goals
  * `-j`: Agent can jump over obstacles i.e. walls
  * `-l <number>`: Limit of visited cells for IDDFS, with `<number>` being a non-negative number (or you can specify this when prompted afterwards)
