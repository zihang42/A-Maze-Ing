import sys
from pathlib import Path

from mazegen import GenerateMethod, MazeGenerator, MazeSolver, SolveMethod
from tests.output_validator import main as validate_output


def test_package(tmp_path: Path) -> None:
    config_path = Path("config.txt")

    maze_generator = MazeGenerator.from_config(str(config_path))
    maze_generator.output_file = str(tmp_path / "output_maze.txt")

    grid = maze_generator.generate(GenerateMethod.BACKTRACKING)

    maze_solver = MazeSolver(grid, maze_generator.entry, maze_generator.exit)
    maze_solver.save(SolveMethod.ASTAR, maze_generator.output_file)

    output_file = Path(maze_generator.output_file)

    assert output_file.exists()
    assert output_file.read_text().strip() != ""


def test_output_file(tmp_path: Path, monkeypatch) -> None:
    output_path = tmp_path / "output_maze.txt"

    maze_generator = MazeGenerator.from_config("config.txt")
    maze_generator.output_file = str(output_path)

    grid = maze_generator.generate(GenerateMethod.BACKTRACKING)

    maze_solver = MazeSolver(grid, maze_generator.entry, maze_generator.exit)
    maze_solver.save(SolveMethod.ASTAR, str(output_path))

    monkeypatch.setattr(sys, "argv", ["output_validator.py", str(output_path)])
    validate_output()
