from mazegen.generator import MazeGenerator


def main() -> None:
    try:
        maze_generator = MazeGenerator.from_config("config.txt")
        maze_generator.generate(None)
        maze_generator.print_maze()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
