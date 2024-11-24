import pytest as pytest

from src.coordinate import Coordinate
from src.maze import Maze

height = 5
width = 5


@pytest.fixture
def simple_maze():
    """
    Простая фикстура для создания лабиринта с заранее известной структурой.
    """
    maze = Maze(height, width, walls_inside=False)
    maze.update_cell(Coordinate(2, 2), left_wall=True, upper_wall=True)
    maze.update_cell(Coordinate(4, 4), left_wall=True, upper_wall=True)
    return maze


@pytest.fixture
def start_finish_coordinates():
    """
    Фикстура для координат начала и конца лабиринта.
    """
    return Coordinate(1, 1), Coordinate(height, width)


@pytest.fixture
def unsolvable_maze():
    """
    Лабиринт без решения — все клетки разделены стенами.
    """
    maze = Maze(height, width)
    for row in range(1, height + 1):
        for col in range(1, width + 1):
            maze.update_cell(Coordinate(row, col), left_wall=True, upper_wall=True)

    return maze
