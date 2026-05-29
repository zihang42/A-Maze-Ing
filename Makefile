UV_LINK_MODE := copy

install:
	uv venv --python 3.13
	source .venv/bin/activate
	UV_LINK_MODE=$(UV_LINK_MODE) uv sync

run:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run a_maze_ing.py config.txt

debug:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -not -path "./.venv*" -name "__pycache__" -exec rm -rf {} +
	find . -not -path "./.venv*" -name ".mypy_cache" -exec rm -rf {} +

lint:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run flake8 . --exclude=.venv,tests,mlx
	UV_LINK_MODE=$(UV_LINK_MODE) uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude "(.venv|mlx|tests)"

lint-strict:
	UV_LINK_MODE=$(UV_LINK_MODE) uv run flake8 . --exclude=.venv,tests,mlx
	UV_LINK_MODE=$(UV_LINK_MODE) uv run mypy . --strict --exclude "(.venv|mlx|tests)"

cow:
	UV_LINK_MODE=$(UV_LINK_MODE) uvx pycowsay hello from uv

build:
	UV_LINK_MODE=$(UV_LINK_MODE) uv build