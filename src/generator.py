import random
from abc import abstractmethod, ABC
from typing import List, Tuple

from src.coordinate import Coordinate, delta, delta_right_down
from src.disjoint_set_union import DisjointSetUnion
from src.maze import Maze

import sys

sys.setrecursionlimit(10_000_000)


class IGenerator(ABC):
    """
    Абстрактный интерфейс для генераторов лабиринтов.
    Все классы, наследующие IGenerator, должны реализовать метод generate.
    """
    @staticmethod
    @abstractmethod
    def generate(height: int, width: int) -> Maze:
        """
        Генерирует лабиринт заданной высоты и ширины.

        Args:
            height (int): Высота лабиринта.
            width (int): Ширина лабиринта.

        Returns:
            Maze: Сгенерированный лабиринт.
        """
        pass


class BacktrackGenerator(IGenerator):
    """
    Генератор лабиринта, использующий алгоритм рекурсивного бэктрекинга.
    """
    @staticmethod
    def recursive_backtrack(cur: Coordinate, maze: Maze):
        """
        Рекурсивный бэктрекинг для генерации лабиринта.

        Args:
            cur (Coordinate): Текущая клетка.
            maze (Maze): Лабиринт.
        """
        maze.update_cell(cur, captured=True)
        possibilities = []

        for d in delta:
            neighbor = Coordinate(cur.row + d[0], cur.col + d[1])
            if maze.coordinate_inside_map(neighbor, consider_auxiliary_area=False):
                possibilities.append(neighbor)

        random.shuffle(possibilities)
        for neighbor in possibilities:
            if maze.get_cell(neighbor).captured:
                continue

            if neighbor.row < cur.row:
                maze.update_cell(cur, upper_wall=False)
            if neighbor.row > cur.row:
                maze.update_cell(neighbor, upper_wall=False)
            if neighbor.col < cur.col:
                maze.update_cell(cur, left_wall=False)
            if neighbor.col > cur.col:
                maze.update_cell(neighbor, left_wall=False)

            BacktrackGenerator.recursive_backtrack(neighbor, maze)

    default_start = Coordinate(1, 1)

    @staticmethod
    def generate(height: int, width: int, start: Coordinate = default_start) -> Maze:
        """
        Генерация лабиринта методом бэктрекинга.

        Args:
            height (int): Высота лабиринта.
            width (int): Ширина лабиринта.
            start (Coordinate): Точка запуска бэктрекинга. По умолчанию (1, 1).

        Returns:
            Maze: Сгенерированный лабиринт.
        """
        if start is None:
            start = BacktrackGenerator.default_start

        maze = Maze(height, width)

        maze.reset_captured()
        BacktrackGenerator.recursive_backtrack(start, maze)
        return maze


class KruskalGenerator(IGenerator):
    """
   Генератор лабиринта, использующий алгоритм Краскала.
   """
    @staticmethod
    def gen_neighbors_pairs(maze: Maze) -> List[Tuple[Coordinate, Coordinate]]:
        """
        Генерирует список пар соседних ячеек лабиринта.

        Args:
            maze (Maze): Лабиринт.

        Returns:
            List[Tuple[Coordinate, Coordinate]]: Список пар соседних ячеек.
        """
        neighbors = []
        for i in range(1, maze.height + 1):
            for j in range(1, maze.width + 1):
                cur = Coordinate(i, j)
                for d in delta_right_down:
                    neighbor = Coordinate(cur.row + d[0], cur.col + d[1])
                    if maze.coordinate_inside_map(neighbor):
                        neighbors.append((cur, neighbor))

        return neighbors

    @staticmethod
    def get_coord_index(coord: Coordinate, maze: Maze):
        """
        Преобразует координаты клетки в одно число - индекс для использования в DSU.

        Args:
            coord (Coordinate): Координата клетки.
            maze (Maze): Лабиринт.

        Returns:
            int: Индекс клетки.
        """
        return (coord.col - 1) * maze.height + (coord.row - 1)

    @staticmethod
    def generate(height: int, width: int) -> Maze:
        """
        Генерация лабиринта методом Краскала.

        Args:
            height (int): Высота лабиринта.
            width (int): Ширина лабиринта.

        Returns:
            Maze: Сгенерированный лабиринт.
        """
        maze = Maze(height, width)
        dsu = DisjointSetUnion(height * width)

        neighbors_pairs = KruskalGenerator.gen_neighbors_pairs(maze)
        random.shuffle(neighbors_pairs)

        for cur, neighbor in neighbors_pairs:
            v = KruskalGenerator.get_coord_index(cur, maze)
            u = KruskalGenerator.get_coord_index(neighbor, maze)

            if dsu.get_set(v) != dsu.get_set(u):
                dsu.unite_sets(v, u)
                if neighbor.row > cur.row:
                    maze.update_cell(neighbor, upper_wall=False)
                if neighbor.col > cur.col:
                    maze.update_cell(neighbor, left_wall=False)

        return maze
