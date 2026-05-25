from .algo.algo_factory import AlgorithmFactory, AlgorithmSolve
from .algo.utils import SolveMethod
from .utils import MazeGrid


class MazeSolver:
    def __init__(
        self,
        grid: MazeGrid,
        entry: tuple[int, int],
        exit: tuple[int, int],
        output_file: str,
        algorithm: SolveMethod = SolveMethod.ASTAR,
    ) -> None:
        self._grid = grid
        self.entry = entry
        self.exit = exit
        self.algorithm = algorithm
        self.output_file = output_file

    def solve(self, method: SolveMethod | None) -> list[tuple[int, int]]:
        if not method:
            method = self.algorithm
        algo = AlgorithmFactory.create(
            method=method, grid=self._grid, entry=self.entry, exit=self.exit
        )
        if isinstance(algo, AlgorithmSolve):
            solution = algo.solve()

        return solution

    def save(self):
        pass
