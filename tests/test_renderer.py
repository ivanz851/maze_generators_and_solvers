import unittest
from src.coordinate import Coordinate
from src.maze import Maze
from src.renderer import ConsoleRenderer


class TestConsoleRenderer(unittest.TestCase):

    def setUp(self):
        self.maze = Maze(3, 3, walls_inside=False)

        self.maze.update_cell(Coordinate(1, 1), left_wall=True, upper_wall=True)
        self.maze.update_cell(Coordinate(1, 2), upper_wall=True)
        self.maze.update_cell(Coordinate(1, 3), upper_wall=True)
        self.maze.update_cell(Coordinate(2, 1), left_wall=True)
        self.maze.update_cell(Coordinate(3, 1), left_wall=True)
        self.maze.update_cell(Coordinate(3, 2))
        self.maze.update_cell(Coordinate(3, 3))

    def test_render_maze_with_path(self):
        path = [Coordinate(1, 1), Coordinate(2, 1), Coordinate(3, 1), Coordinate(3, 2), Coordinate(3, 3)]
        rendered_maze_with_path = ConsoleRenderer.render(self.maze, path)

        ConsoleRenderer.print_to_console(self.maze, path)

        self.assertEqual(rendered_maze_with_path[1][2], 'S')
        self.assertEqual(rendered_maze_with_path[3][2], '*')
        self.assertEqual(rendered_maze_with_path[5][2], '*')
        self.assertEqual(rendered_maze_with_path[5][6], '*')
        self.assertEqual(rendered_maze_with_path[5][10], 'F')

    def test_expand_horizontally(self):
        tiny_repr = ConsoleRenderer.render_tiny(self.maze)
        expanded_repr = ConsoleRenderer.expand_horizontally(tiny_repr)

        self.assertEqual(len(expanded_repr[0]), len(tiny_repr[0]) * 2 - 1)

    def test_expand_vertically(self):
        tiny_repr = ConsoleRenderer.render_tiny(self.maze)
        expanded_repr_horizontally = ConsoleRenderer.expand_horizontally(tiny_repr)
        expanded_repr_vertically = ConsoleRenderer.expand_vertically(expanded_repr_horizontally)

        self.assertEqual(len(expanded_repr_vertically), len(expanded_repr_horizontally) * 2 - 1)
