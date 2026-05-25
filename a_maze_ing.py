from mazegen.generator import MazeGenerator


def main() -> None:
    '''
        The main function that will create and handle
        all the a_maze_ing
    '''
    try:
        maze_generator = MazeGenerator.from_config("config.txt")
        maze_generator.generate(None)
        maze_generator.print_maze()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
