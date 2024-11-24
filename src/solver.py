from abc import ABC, abstractmethod
from collections import deque
from typing import List, Tuple

from src.coordinate import Coordinate, delta
from src.maze import Maze


class ISolver(ABC):
    @staticmethod
    @abstractmethod
    def solve(maze: Maze, start: Coordinate, finish: Coordinate) -> List[Coordinate]:
        """
        Решает лабиринт, возвращая маршрут от стартовой до конечной координаты.

        Args:
            maze (Maze): Лабиринт, в котором нужно найти путь.
            start (Coordinate): Начальная координата.
            finish (Coordinate): Конечная координата.

        Returns:
            List[Coordinate]: Список координат, представляющих путь от старта до финиша.
        """
        pass


class BacktrackSolver(ISolver):
    @staticmethod
    def solve(maze: Maze, start: Coordinate, finish: Coordinate) -> Tuple[bool, List[Coordinate]]:
        """
        Решает лабиринт с использованием метода бэктрекинга.

        Args:
            maze (Maze): Лабиринт, в котором нужно найти путь.
            start (Coordinate): Начальная координата.
            finish (Coordinate): Конечная координата.

        Returns:
            Tuple[bool, List[Coordinate]]: Возвращает кортеж, где:
                - bool: True, если путь найден, иначе False.
                - List[Coordinate]: Список координат, представляющих найденный путь (если путь найден).
        """

        path = []

        maze.reset_captured()
        BacktrackSolver.recursive_backtrack(start, finish, maze, path)
        return len(path) > 0, path

    @staticmethod
    def reached_finish(path: List[Coordinate], finish: Coordinate) -> bool:
        """
        Проверяет, достиг ли путь конечной координаты.

        Args:
            path (List[Coordinate]): Текущий маршрут.
            finish (Coordinate): Конечная координата.

        Returns:
            bool: True, если путь достиг финиша, иначе False.
        """
        return len(path) > 0 and path[-1] == finish

    @staticmethod
    def recursive_backtrack(cur: Coordinate, finish: Coordinate, maze: Maze, path: List[Coordinate]) -> None:
        """
        Метод для поиска пути с помощью рекурсивного бэктрекинга.

        Args:
            cur (Coordinate): Текущая координата.
            finish (Coordinate): Конечная координата.
            maze (Maze): Лабиринт, в котором осуществляется поиск.
            path (List[Coordinate]): Список координат, представляющих путь.
        """

        maze.update_cell(cur, captured=True)
        path.append(cur)

        if BacktrackSolver.reached_finish(path, finish):
            return

        possibilities = []

        for d in delta:
            neighbor = Coordinate(cur.row + d[0], cur.col + d[1])
            if maze.coordinate_inside_map(neighbor):
                possibilities.append(neighbor)

        for neighbor in possibilities:
            if maze.get_cell(neighbor).captured or maze.check_wall(cur, neighbor):
                continue

            BacktrackSolver.recursive_backtrack(neighbor, finish, maze, path)
            if BacktrackSolver.reached_finish(path, finish):
                return

        path.pop()


class BreadthFirstSearchSolver(ISolver):
    @staticmethod
    def solve(maze: Maze, start: Coordinate, finish: Coordinate) -> Tuple[bool, List[Coordinate]]:
        """
        Решает лабиринт с использованием поиска в ширину (BFS).

        Args:
            maze (Maze): Лабиринт, в котором нужно найти путь.
            start (Coordinate): Начальная координата.
            finish (Coordinate): Конечная координата.

        Returns:
            Tuple[bool, List[Coordinate]]: Возвращает кортеж, где:
                - bool: True, если путь найден, иначе False.
                - List[Coordinate]: Список координат, представляющих найденный путь (если путь найден).
        """

        queue = deque([start])
        parent = {start: None}

        while queue:
            cur = queue.popleft()
            if cur == finish:
                break

            for d in delta:
                neighbor = Coordinate(cur.row + d[0], cur.col + d[1])
                if maze.coordinate_inside_map(neighbor, consider_auxiliary_area=False) and neighbor not in parent and \
                        not maze.check_wall(cur, neighbor):
                    queue.append(neighbor)
                    parent[neighbor] = cur

        path = []
        if finish in parent:
            cur = finish
            while cur:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return True, path
        else:
            return False, path
