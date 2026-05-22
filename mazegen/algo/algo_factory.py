from .astar import AstartSolve
from .backtracking import BacktrackingGen
from .utils import AlgorithmGen, AlgorithmSolve, GenerateMethod, SolveMethod


class AlgorithmFactory:
    _registry: dict[
        GenerateMethod | SolveMethod, type[AlgorithmGen] | type[AlgorithmSolve]
    ] = {
        GenerateMethod.BACKTRACKING: BacktrackingGen,
        SolveMethod.ASTAR: AstartSolve,
    }

    @classmethod
    def create(
        cls, method: GenerateMethod | SolveMethod, **kwargs
    ) -> AlgorithmGen | AlgorithmSolve:
        algo = cls._registry.get(method)
        if not algo:
            raise ValueError("Update the AlgorithmFactory!")
        return algo(**kwargs)
