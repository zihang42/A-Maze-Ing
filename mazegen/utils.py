from dataclasses import dataclass
from enum import Enum

import numpy as np

PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]


class Direction(Enum):
    """
    breakdown on NORTH:
    -1: go towards the north direction which means move up one row
    0: stay on the same column
    0: the index of Direction, north is 0, break current cell northern wall
    2: the index of Direction, south is 2, break target cell southern wall
    """

    NORTH = (-1, 0, 0, 2)
    EAST = (0, 1, 1, 3)
    SOUTH = (1, 0, 2, 0)
    WEST = (0, -1, 3, 1)


DIRECTIONS = [d.value for d in Direction]


@dataclass
class MazeGrid:
    walls: np.ndarray
    blocked: np.ndarray

    @property
    def shape(self) -> tuple[int, int]:
        return self.walls.shape[:2]

    @property
    def size(self) -> int:
        height, width = self.shape
        return height * width
