import random
from mlx import Mlx
from mazegen.utils import MazeGrid


'''
    Definition of the constants
    that will be used in the visualizer
'''
CELL_SIZE = 40
COLOR_BG = 0xFF000000        # Black
COLOR_42 = 0xFF1B4D22        # Deep green
WALL_COLOR = 0xFF2D7A27      # Lite green
COLOR_ENTRY = 0xFF5BF542     # Fluorecent green
COLOR_EXIT = 0xFFF54242      # Red
COLOR_PATH = 0xFF8CA3F5      # Ligth blue
AL = 0xFF000000


def handle_key(keynum: int, visualizer: MazeVisualizer) -> None:
    '''
        Each time a key is presed this function is called

        Args:
            keynum: The identification of the presed key
            visualizer: The instance of the MazeVisualizer
                        class

        Examples:
            When you press the 'q' key the handle_key function
            is called with a keynum of 113, it triger the first
            if statment which clean and exit the program

        Key_value used:
            113 for 'q'
            65307 for 'esc'
            50 for '2'
            52 for '4'
            51 for '3'
            49 for '1'
    '''
    if keynum in (65307, 113, 52):
        visualizer.clean()
        return
    elif keynum == 50:
        visualizer.show_path = not visualizer.show_path
        visualizer.generate_maze_image()
        visualizer.reset_window()
    elif keynum == 51:
        global COLOR_42
        global WALL_COLOR
        global COLOR_ENTRY
        global COLOR_EXIT
        global COLOR_PATH
        COLOR_42 = random.randint(0, 0xFFFFFF) | AL
        WALL_COLOR = random.randint(0, 0xFFFFFF) | AL
        COLOR_ENTRY = random.randint(0, 0xFFFFFF) | AL
        COLOR_EXIT = random.randint(0, 0xFFFFFF) | AL
        COLOR_PATH = random.randint(0, 0xFFFFFF) | AL
        visualizer.generate_maze_image()
        visualizer.reset_window()
    elif keynum == 49:
        visualizer.reset_window()


def handle_expose(visualizer: MazeVisualizer) -> None:
    '''
        This function is called by MiniLibX
        when the window need to be displayed

        It's used to push the MLX image to the window

        Args:
            visualizer: The instance of the MazeVisualizer
                        class
    '''
    visualizer.reset_window()


def handle_close(visualizer: MazeVisualizer) -> None:
    '''
        This function is called when the user click
        on the close button

        It free all the allocated memory by MLX under
        the hood and exit

        Args:
            visualizer: The instance of the MazeVisualizer
                        class
    '''
    visualizer.clean()
    return


class MazeVisualizer:

    '''
        The class of our visualizer, it's the graphical
        motor that use MiniLibX

        - It initiate the MiniLibX instance
        - Create the MiniLibX Maze image
        - Launch the loop and display the image

        Attributes:
            grid(object):    The instance of the maze grid
            entry(tuple):    The coord of the maze entry
            exit(tuple):     The coord of the maze exit
            path(tuples):    The path of cells to solve the maze
            show_path(bool): A boolean to show the path or not
            rows,cols(ints): The rows and cols size of the grid
            win_width(int):  The width of the win based on the
                             cells size
            win_height(int): Same for the height
            m(object):       The instance of the MLX class
            mlx_ptr(a ptr):  The address of the MLX server
            win_ptr(a ptr):  The address of the maze window
            img_ptr(a ptr):  The adress of the MLX image (RAM=>VRAM)
            img_data(tuples):All the bites of our image
            bpp(int):        Bits per pixel (32 bits so 4 bites)
            size_line(int):  The nb of bites in a line of our image
            endian(int):     Is in Little Endian so we are on BGRA
    '''
    def __init__(self, grid: MazeGrid, entry: tuple[int, int],
                 exit_coord: tuple[int, int]) -> None:
        '''
            After initializing the variable we call the
            function generate_maze_image and setup the hooks
        '''
        # Base Maze data
        self.grid = grid
        self.entry = entry
        self.exit = exit_coord
        self.path: list[tuple[int, int]] = []
        self.show_path = True
        self.rows, self.cols = grid.shape
        self.win_width = self.cols * CELL_SIZE
        self.win_height = self.rows * CELL_SIZE + (CELL_SIZE * 2)

        # Creation of the MiniLibX window and image
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.win_width,
            self.win_height, "A-Maze-ing Buffering"
        )
        self.img_ptr = self.m.mlx_new_image(
            self.mlx_ptr, self.win_width, self.win_height
        )
        self.img_data, self.bpp, \
            self.size_line, self.endian = \
            self.m.mlx_get_data_addr(
                self.img_ptr
            )
        self.generate_maze_image()
        self.m.mlx_key_hook(
            self.win_ptr, handle_key, self
        )
        self.m.mlx_expose_hook(
            self.win_ptr, handle_expose, self
        )
        self.m.mlx_hook(
            self.win_ptr, 33, 0, handle_close, self
        )

    def set_path(self, path: list[tuple[int, int]]) -> None:
        '''
            The function called in main to set the path
        '''
        self.path = path
        self.generate_maze_image()

    def fill_pixel(self, x: int, y: int, color: int) -> None:
        '''
            The smart bitwise function that make us
            fill the color in the right index (BGRA)
            >> rotate to the wright the bits
            & take only the last 8 bit !!
        '''
        index = (y * self.size_line) + (x * 4)
        self.img_data[index] = color & 0xFF
        self.img_data[index + 1] = (color >> 8) & 0xFF
        self.img_data[index + 2] = (color >> 16) & 0xFF
        self.img_data[index + 3] = (color >> 24) & 0xFF

    def draw(self, x: int, y: int, width: int,
             height: int, color: int) -> None:
        '''
            This function will fill pixels in the given
            area

            Args:
                color:  The given color in hex
                height: The height of the cell
                        to fill
                width:  The width of the cell to
                        fill
                x:      The position of the pixel
                        horiontaly
                y:      The position of the pixel
                        verticaly
        '''
        for i in range(height):
            for j in range(width):
                self.fill_pixel(x + j, y + i, color)

    def draw_walls(self, row: int, col: int, walls: list[bool]) -> None:
        '''
            Draw walls if the bool is True

            Args:
                row: The actual row beging check
                col: The actual colums beging check
                walls: The bool list for the current cell
        '''
        # We set x and y to the uper left of the block
        x = col * CELL_SIZE
        y = row * CELL_SIZE

        if walls[0]:
            self.draw(x, y, CELL_SIZE, 2, WALL_COLOR)
        if walls[1]:
            self.draw(x + CELL_SIZE - 2, y, 2, CELL_SIZE, WALL_COLOR)
        if walls[2]:
            self.draw(x, y + CELL_SIZE - 2, CELL_SIZE, 2, WALL_COLOR)
        if walls[3]:
            self.draw(x, y, 2, CELL_SIZE, WALL_COLOR)

    def generate_maze_image(self) -> None:
        '''
            This function apply 4 layer of pixel on the window

            layer 1:
                Go trough all the colums of the rows and draw
                when on the 42 pattern else draw background

            layer 2:
                Draw the path color on each coords of the path
                except for the start and exit

            layer 3:
                Draw the start and exit

            layer 4:
                Go trough each colums of rows and draw the walls
                by calling the special draw wall function with
                the boolean set for each cells
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                color = COLOR_42 if self.grid.blocked[row][col] else COLOR_BG
                self.draw(
                    col * CELL_SIZE, row * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE, color
                )
        if self.show_path and self.path:
            for row, col in self.path:
                if (row, col) != self.entry and (row, col) != self.exit:
                    self.draw(
                        col * CELL_SIZE + 4, row * CELL_SIZE + 4,
                        CELL_SIZE - 8, CELL_SIZE - 8, COLOR_PATH
                    )
        self.draw(
            self.entry[1] * CELL_SIZE + 3, self.entry[0] * CELL_SIZE + 3,
            CELL_SIZE - 3, CELL_SIZE - 3, COLOR_ENTRY
        )
        self.draw(
            self.exit[1] * CELL_SIZE + 3, self.exit[0] * CELL_SIZE + 3,
            CELL_SIZE - 3, CELL_SIZE - 3, COLOR_EXIT
        )
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_walls(row, col, self.grid.walls[row][col])

    def reset_window(self) -> None:
        '''
            Function called at the begining and each time
            there is modification to push back the modified
            MLX image
        '''
        self.m.mlx_put_image_to_window(
            self.mlx_ptr,
            self.win_ptr,
            self.img_ptr,
            0,
            0
        )
        self.m.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            self.win_width // 4,
            (self.rows * CELL_SIZE) + (CELL_SIZE),
            0xFFFFFF,
            "1: refresh 2: path 3: color 4: quit"
        )

    def start(self) -> None:
        '''
            Launch the MLX loop
            called in main
        '''
        self.m.mlx_loop(
            self.mlx_ptr
        )

    def clean(self) -> None:
        '''
            The called function to exit the program
            it clean the MLX allocation that the lib
            did under the hood
        '''
        self.m.mlx_destroy_image(
            self.mlx_ptr, self.img_ptr
        )
        self.m.mlx_destroy_window(
            self.mlx_ptr, self.win_ptr
        )
        self.m.mlx_release(
            self.mlx_ptr
        )
