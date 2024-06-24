# COS30019 Assignment 1 - Tree Based Search for Robot Navigation Problem

## Introduction

This is the source code for the Assignment 1 of course unit COS30019 - Introduction to Artificial Intelligence. Written in Python (3.12.0), the program implements tree-based search algorithms to search for solutions to the Robot Navigation problem, with both informed and uninformed methods.

### General Information

- Programming language: Python 3.12.0
- The algorithms have an option to find path for ALL goals
- The agent has an optional ability to jump over obstacles

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
  python3 search.py <filename> <algorithm>
  ```
* Windows:

  ```
  python search.py <filename> <algorithm>
  ```
  Replace `<filename>` with a filename in the ***maps*** folder, and `<algorithm>` with an algorithm name. For example, for BFS search using map in file *RobotNav-test.txt* on Windows:

  ```
  python search.py RobotNav-test.txt bfs
  ```
  Output follows the standard stated in the assignment instruction. For help and more information, running the command:

  ```
  python search.py help
  ```
  It will show lists of names for available search algorithms, map files, and optional tags.

  ### Algorithm names


  - `bfs` for BFS
  - `dfs` for DFS
  - `iddfs` for IDDFS
  - `greedy` for GBFS
  - `astar` for A* Search
  - `bi_astar` for Bidirectional A* Search

  ### Optional tags

  - `-a`: Search all goals
  - `-j`: Agent can jump over obstacles
  - `-l`: Limit of visited cells for IDDFS (or you can specify this when prompted afterwards)
