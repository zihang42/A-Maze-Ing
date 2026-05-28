install:
	uv venv
	uv pip install -r pyproject.toml

run:
	uv run a_maze_ing.py config.txt

debug:
	uv run python3 -m pdb a_maze_ing.py

clean:
	find . -not -path "./.venv*" -name "__pycache__" -exec rm -rf {} +
	find . -not -path "./.venv*" -name ".mypy_cache" -exec rm -rf {} +

lint:
	uv run flake8 . --exclude=.venv,tests,mlx
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude "(.venv|mlx|tests)"

lint-strict:
	uv run flake8 . --exclude=.venv,tests,mlx
	uv run mypy . --strict --exclude "(.venv|mlx|tests)"

cow:
	uvx pycowsay hello from uv
