import unittest
from unittest.mock import patch
from src.user_interaction import UserInteraction
from src.coordinate import Coordinate


class TestUserInteraction(unittest.TestCase):
    @patch('builtins.input', side_effect=['3'])
    def test_read_natural_number(self, mock_input):
        result = UserInteraction.read_natural_number()
        self.assertEqual(result, 3)

    @patch('builtins.input', side_effect=['0', '5', '2'])
    def test_read_natural_number_with_restriction(self, mock_input):
        result = UserInteraction.read_natural_number(max_restr=5)
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=[f'{UserInteraction.GeneratorAlgorithm.BACKTRACKING.value}'])
    @patch('src.user_interaction.UserInteraction.get_cell_coords', return_value=Coordinate(4, 5))
    def test_read_generator_params_backtracking(self, mock_get_cell_coords, mock_input):
        height, width = 10, 10
        generator_algorithm, start_coordinate = UserInteraction.read_generator_params(height, width)

        self.assertEqual(generator_algorithm, UserInteraction.GeneratorAlgorithm.BACKTRACKING)
        self.assertEqual(start_coordinate, Coordinate(4, 5))

    @patch('builtins.input', side_effect=[f'{UserInteraction.GeneratorAlgorithm.KRUSKAL.value}'])
    def test_read_generator_params_kruskal(self, mock_input):
        height, width = 10, 10
        generator_algorithm, start_coordinate = UserInteraction.read_generator_params(height, width)

        self.assertEqual(generator_algorithm, UserInteraction.GeneratorAlgorithm.KRUSKAL)
        self.assertIsNone(start_coordinate)

    @patch('builtins.input', side_effect=[f'{UserInteraction.SolverAlgorithm.BACKTRACKING.value}', '2'])
    @patch('src.user_interaction.UserInteraction.get_cell_coords', return_value=Coordinate(1, 1))
    def test_read_solver_params_backtracking(self, mock_get_cell_coords, mock_input):
        height, width = 10, 10
        solver_algorithm, start, finish = UserInteraction.read_solver_params(height, width)

        self.assertEqual(solver_algorithm, UserInteraction.SolverAlgorithm.BACKTRACKING)
        self.assertEqual(start, Coordinate(1, 1))
        self.assertEqual(finish, Coordinate(1, 1))

    @patch('builtins.input', side_effect=['3', '0', f'{UserInteraction.SolverAlgorithm.BFS.value}',
                                          f'{UserInteraction.SolverAlgorithm.BACKTRACKING.value}'])
    @patch('src.user_interaction.UserInteraction.get_cell_coords', return_value=Coordinate(2, 2))
    def test_read_solver_params_bfs(self, mock_get_cell_coords, mock_input):
        height, width = 10, 10
        solver_algorithm, start, finish = UserInteraction.read_solver_params(height, width)

        self.assertEqual(solver_algorithm, UserInteraction.SolverAlgorithm.BFS)
        self.assertEqual(start, Coordinate(2, 2))
        self.assertEqual(finish, Coordinate(2, 2))
