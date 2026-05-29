*This activity has been created as part of the 42 curriculum by ziwang, lcoant--*

# A_Maze_Ing

## Description
A maze generator in Python that takes a configuration file, generates a
maze and writes it to a file
using a hexadecimal wall representation. The visual representation is provided.

## Instruction

### Create venv

```
make install
source ./venv/bin/activate
```

### Install depandencies

```
uv sync
```

### Build package

```
uv build
uv pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Usage
So now we only have to do this?
'''
make run
'''
#### Load from config
```python
from mazegen import GenerateMethod, MazeGenerator, MazeSolver, SolveMethod

maze_generator = MazeGenerator.from_config(str(config_path))
grid = maze_generator.generate(GenerateMethod.BACKTRACKING)
maze_solver = MazeSolver(grid, maze_generator.entry, maze_generator.exit)
maze_solver.save(SolveMethod.ASTAR, maze_generator.output_file)
```

#### Init an instance
```python
from mazegen import GenerateMethod, MazeGenerator, MazeSolver, SolveMethod

# Your config here
maze_generator = MazeGenerator(...)
grid = maze_generator.generate(GenerateMethod.BACKTRACKING)
maze_solver = MazeSolver(grid, maze_generator.entry, maze_generator.exit)
maze_solver.save(SolveMethod.ASTAR, maze_generator.output_file)
```

## Blablabla
* Package manager: UV, it is the best
* Git:
  * use `git pull origin main --rebase` to keep our commits linear
  * work on the feature branch first `git switch -c XXX` then send a PR to the main

## Resources
1. [Gen&Solve algorithm](https://emmilco.github.io/path_finder/)
2. [Gen algorithm](https://www.jamisbuck.org/mazes/)
3. [A* algorithm](https://www.datacamp.com/tutorial/a-star-algorithm)

## Contributions
*Ziwang:*
* Maze generator
* Maze solver
*Lohann:*
- Visualizor
- Makefile things
