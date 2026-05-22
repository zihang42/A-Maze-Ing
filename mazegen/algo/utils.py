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
