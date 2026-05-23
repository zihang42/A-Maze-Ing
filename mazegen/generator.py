import random
from typing import Self

import numpy as np

from src.parser import Parser

from .algo.algo_factory import AlgorithmFactory
from .algo.utils import AlgorithmGen, GenerateMethod
from .utils import PATTERN_42, MazeGrid


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        algorithm: GenerateMethod = GenerateMethod.BACKTRACKING,
        seed: int = 42,
        perfect: bool = True,
        display_42: bool = True,
        output_file: str | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.algorithm = algorithm
        self.seed = seed
        self.perfect = perfect
        self.display_42 = display_42
        self.output_file = output_file
        self._grid = MazeGrid(
            np.ones((self.height, self.width, 4), dtype=bool),
            np.zeros((self.height, self.width), dtype=bool),
        )
        self._visited = np.zeros((self.height, self.width), dtype=bool)
        random.seed(seed)

    @classmethod
    def from_config(cls, path: str) -> Self:
        parser = Parser(path)
        config = parser.to_config()
        return cls(**config.model_dump())

    def generate(self, method: GenerateMethod | None) -> MazeGrid:
        if method is None:
            method = self.algorithm
        if self.display_42:
            self._apply_42_pattern()
        algo = AlgorithmFactory.create(
            method,
            grid=self._grid,
            visited=self._visited,
            start=self.entry,
        )
        if isinstance(algo, AlgorithmGen):
            algo.generate()
        if not self.perfect:
            self._imperfect()
        return self._grid

    def _apply_42_pattern(self) -> None:
        height_42, width_42 = len(PATTERN_42), len(PATTERN_42[0])
        if self.height < height_42 or self.width < width_42:
            raise ValueError(
                f"maze size {self.width}x{self.height} is too small for "
                f"42 pattern {width_42}x{height_42}"
            )
        h_start = (self.height - height_42) // 2
        w_start = (self.width - width_42) // 2
        cells = []
        for height in range(height_42):
            for width in range(width_42):
                if PATTERN_42[height][width] == 1:
                    coord = (h_start + height, w_start + width)
                    if coord == self.entry:
                        raise ValueError(
                            f"42 pattern is overlapped with entry: {coord}"
                        )
                    elif coord == self.exit:
                        raise ValueError(
                            f"42 pattern is overlapped with exit: {coord}"
                        )
                    cells.append(coord)
        for x, y in cells:
            self._grid.blocked[x][y] = True

    def print_maze(self) -> None:
        grid = self._grid.walls
        h, w = grid.shape[0], grid.shape[1]
        print("+" + "---+" * w)
        for i in range(h):
            row = "|"
            for j in range(w):
                if (i, j) == self.entry:
                    cell = " E "
                elif (i, j) == self.exit:
                    cell = " X "
                elif self._grid.blocked[i][j]:
                    cell = "###"
                else:
                    cell = "   "
                if grid[i][j][1]:
                    row += cell + "|"
                else:
                    row += cell + " "
            print(row)
            bottom = "+"
            for j in range(w):
                if grid[i][j][2]:
                    bottom += "---+"
                else:
                    bottom += "   +"
            print(bottom)

    def _imperfect(self):
        """
        #TODO:
        WIP
        """
        pass
