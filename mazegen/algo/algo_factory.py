from .astar import AstarSolve
from .backtracking import BacktrackingGen
from .utils import AlgorithmGen, AlgorithmSolve, GenerateMethod, SolveMethod


class AlgorithmFactory:
    _registry: dict[
        GenerateMethod | SolveMethod, type[AlgorithmGen] | type[AlgorithmSolve]
    ] = {
        GenerateMethod.BACKTRACKING: BacktrackingGen,
        SolveMethod.ASTAR: AstarSolve,
    }

    @classmethod
    def create(
        cls, method: GenerateMethod | SolveMethod, **kwargs
    ) -> AlgorithmGen | AlgorithmSolve:
        algo = cls._registry.get(method)
        if not algo:
            raise ValueError("Update the AlgorithmFactory!")
        return algo(**kwargs)
