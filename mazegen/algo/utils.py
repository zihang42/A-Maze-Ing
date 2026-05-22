from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

import numpy as np

from mazegen.generator import MazeGrid
from mazegen.utils import DIRECTIONS


class GenerateMethod(Enum):
    BACKTRACKING = "backtracking"
    PRIM = "prim"


class SolveMethod(Enum):
    BFS = "bfs"
    DFS = "dfs"
    ASTAR = "astar"


@dataclass
class AlgorithmGen(ABC):
    grid: MazeGrid
    visited: np.ndarray
    start: tuple[int, int]
    direction: list[tuple[int, int, int, int]] = field(
        default_factory=lambda: list(DIRECTIONS)
    )

    @abstractmethod
    def generate(self) -> None:
        pass


@dataclass
class AlgorithmSolve(ABC):
    grid: MazeGrid
    entry: tuple[int, int]
    exit: tuple[int, int]

    @abstractmethod
    def solve(self) -> list[tuple[int, int]]:
        pass


def is_blocked(grid: MazeGrid, coord: tuple[int, int]) -> bool:
    return grid.blocked[coord[0], coord[1]]


def is_in_bound(grid: MazeGrid, row: int, col: int) -> bool:
    return 0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]

def open_wall(grid: MazeGrid, row: int, col: int, wall_index: int) -> None:
    grid.walls[row, col, wall_index] = False