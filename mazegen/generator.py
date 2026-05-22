from typing import Self

import numpy as np

from src.parser import Parser

from .algo.algo_factory import AlgorithmFactory
from .algo.utils import AlgorithmGen, GenerateMethod
from .utils import MazeGrid


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

    @classmethod
    def from_config(cls, path: str) -> Self:
        parser = Parser(path)
        config = parser.to_config()
        return cls(**config.model_dump())

    def generate(self, method: GenerateMethod | None) -> MazeGrid:
        if not method:
            method = self.algorithm
        if self.display_42:
            self._apply_42_pattern()
        try:
            algo = AlgorithmFactory.create(
                method, grid=self._grid, visited=self._visited
            )
            if isinstance(algo, AlgorithmGen):
                algo.generate()
        except ValueError as e:
            print(e)
        if not self.perfect:
            self._imperfect()
        return self._grid

    def _apply_42_pattern(self):
        """
        #TODO:
        Append 42Pattern into visited
        """
        pass

    def _imperfect(self):
        """
        #TODO:
        WIP
        """
        pass
