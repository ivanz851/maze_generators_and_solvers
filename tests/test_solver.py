from src.solver import BreadthFirstSearchSolver, BacktrackSolver


class TestBacktrackSolver:
    def test_backtrack_solver_simple_maze(self, simple_maze, start_finish_coordinates):
        start, finish = start_finish_coordinates
        found, path = BacktrackSolver.solve(simple_maze, start, finish)
        assert found, "Backtracking должен найти путь в простом лабиринте"

    def test_backtrack_solver_unsolvable_maze(self, unsolvable_maze, start_finish_coordinates):
        start, finish = start_finish_coordinates
        found, path = BacktrackSolver.solve(unsolvable_maze, start, finish)
        assert not found, "В неразрешимом лабиринте пути не существует."


class TestBreadthFirstSearchSolver:
    def test_bfs_solver_simple_maze(self, simple_maze, start_finish_coordinates):
        start, finish = start_finish_coordinates
        found, path = BreadthFirstSearchSolver.solve(simple_maze, start, finish)
        assert found, "BFS должен найти путь в простом лабиринте"
        assert path[0] == start
        assert path[-1] == finish

    def test_bfs_solver_unsolvable_maze(self, unsolvable_maze, start_finish_coordinates):
        start, finish = start_finish_coordinates
        found, path = BreadthFirstSearchSolver.solve(unsolvable_maze, start, finish)
        assert not found, "В неразрешимом лабиринте пути не существует."