import random
import sys

from mazegen import GenerateMethod, MazeGenerator, MazeGrid
from mazegen import MazeSolver
from src.visualisor import MazeVisualizer


def main() -> None:
    """
    The main function that will create and handle
    all the a_maze_ing
    """
    if len(sys.argv) != 2:
        return
    path = sys.argv[1].strip()
    try:
        maze_generator = MazeGenerator.from_config(path)

        def regenerate_maze() -> tuple[MazeGrid, list[tuple[int, int]]]:
            method = random.choice(list(GenerateMethod))

            new_generator = MazeGenerator.from_config(path)
            new_grid = new_generator.generate(method)

            new_solver = MazeSolver(
                new_grid,
                new_generator.entry,
                new_generator.exit,
            )
            new_path = new_solver.save(None, new_generator.output_file)

            return new_grid, new_path

        grid, path_full = regenerate_maze()

        viz = MazeVisualizer(
            grid,
            maze_generator.entry,
            maze_generator.exit,
            regenerate_maze,
        )

        viz.set_path(path_full)
        viz.start()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
