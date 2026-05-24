from enum import Enum


class GenerateMethod(Enum):
    BACKTRACKING = "backtracking"
    PRIM = "prim"


class SolveMethod(Enum):
    BFS = "bfs"
    DFS = "dfs"
    ASTAR = "astar"
