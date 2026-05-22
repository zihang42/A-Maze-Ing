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
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.algorithm = algorithm
        self.seed = seed
        self.perfect = perfect
        self.display_42 = display_42
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
        if not method:
            method = self.algorithm
        if self.display_42:
            try:
                self._apply_42_pattern()
            except ValueError as e:
                print(e)
        try:
            algo = AlgorithmFactory.create(
                method,
                grid=self._grid,
                visited=self._visited,
                start=self.entry,
            )
            if isinstance(algo, AlgorithmGen):
                algo.generate()
        except ValueError as e:
            print(e)
        if not self.perfect:
            self._imperfect()
        return self._grid

    def _apply_42_pattern(self):
        height_42, width_42 = len(PATTERN_42), len(PATTERN_42[0])
        if height_42 < 8 or width_42 < 8:
            raise ValueError(
                "to apply 42 pattern, the minimum size of maze is 8X8"
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

    def _imperfect(self):
        """
        #TODO:
        WIP
        """
        pass
