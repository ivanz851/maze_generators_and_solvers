import os
from enum import Enum
from typing import Tuple, Optional

from src.coordinate import Coordinate
from src.generator import KruskalGenerator, BacktrackGenerator
from src.maze import Maze
from src.renderer import ConsoleRenderer
from src.solver import BacktrackSolver, BreadthFirstSearchSolver


class UserInteraction:
    class GeneratorAlgorithm(Enum):
        """
        Перечисление методов генерации лабиринта с описанием.
        """
        BACKTRACKING = (1, "Метод рекурсивного бэктрекинга")
        KRUSKAL = (2, "Алгоритм Краскала")

        def __init__(self, value, description):
            self._value_ = value
            self.description = description

    class SolverAlgorithm(Enum):
        """
        Перечисление методов решения лабиринта с описанием.
        """
        BACKTRACKING = (1, "Метод рекурсивного бэктрекинга")
        BFS = (2, "Поиск в ширину")

        def __init__(self, value, description):
            self._value_ = value
            self.description = description

    @staticmethod
    def read_maze_params_and_gen_maze() -> None:
        """
        Считывание параметров лабиринта (размеры и метод генерации) и решение с использованием выбранного метода.

        Генерирует лабиринт на основе введённых пользователем параметров, решает его с использованием
        выбранного алгоритма, выводит результат (найден ли путь) и визуализирует лабиринт с маршрутом.

        Returns:
            None
        """

        height, width = UserInteraction.read_height_width()
        generator_params = UserInteraction.read_generator_params(height, width)

        maze: Maze = Maze(height, width)
        if generator_params[0] == UserInteraction.GeneratorAlgorithm.BACKTRACKING:
            maze = BacktrackGenerator.generate(height, width, generator_params[1])
        elif generator_params[0] == UserInteraction.GeneratorAlgorithm.KRUSKAL:
            maze = KruskalGenerator.generate(height, width)

        solver_method, start, finish = UserInteraction.read_solver_params(height, width)

        ok: bool = False
        path: list[Coordinate] = []
        if solver_method == UserInteraction.SolverAlgorithm.BACKTRACKING:
            ok, path = BacktrackSolver.solve(maze, start, finish)
        elif solver_method == UserInteraction.SolverAlgorithm.BFS:
            ok, path = BreadthFirstSearchSolver.solve(maze, start, finish)

        if ok:
            print("\nПуть найден!\n")
            ConsoleRenderer.print_to_console(maze, path)
        else:
            print("\nПуть не найден!")
            ConsoleRenderer.print_to_console(maze)

    @staticmethod
    def read_height_width() -> Tuple[int, int]:
        """
        Считывание высоты и ширины лабиринта с проверкой корректности ввода.

        Высота и ширина — это натуральные числа. Лабиринт должен состоять по крайней мере из 2 клеток.

        Returns:
            Tuple[int, int]: Высота и ширина лабиринта.
        """

        UserInteraction.clear_console()
        msg = "Введите одно натуральное число - высоту лабиринта."
        print(msg)
        height = UserInteraction.read_natural_number()

        msg = "Введите одно натуральное число - ширину лабиринта."
        print(msg)

        msg_width_restr = ""
        if height == 1:
            msg_width_restr += "Лабиринт должен состоять по крайней мере из 2 клеток, поэтому ширина должна быть " \
                               "не меньше 2.\n"
        width = 0
        while (height > 1 and width == 0) or (height == 1 and width < 2):
            print(msg_width_restr, end='')
            width = UserInteraction.read_natural_number()

        print(f"OK! Высота: {height}, ширина: {width}")

        return height, width

    @staticmethod
    def read_generator_params(height: int, width: int) -> Tuple[GeneratorAlgorithm, Optional[Coordinate]]:
        """
        Считывание метода генерации лабиринта и параметров для метода бэктрекинга (координаты стартовой клетки),
        если выбран метод генерации бэктрекингом.

        Args:
            height (int): Высота лабиринта.
            width (int): Ширина лабиринта.

        Returns:
            Tuple[GeneratorAlgorithm, Optional[Coordinate]]: Выбранный метод генерации и координаты стартовой клетки
            для метода бэктрекинга (или None, если выбран другой метод).
        """

        UserInteraction.clear_console()
        msg = f"Выберите метод генерации лабиринта: " \
              f"{UserInteraction.GeneratorAlgorithm.BACKTRACKING.value} - " \
              f"{UserInteraction.GeneratorAlgorithm.BACKTRACKING.description}, " \
              f"{UserInteraction.GeneratorAlgorithm.KRUSKAL.value} - " \
              f"{UserInteraction.GeneratorAlgorithm.KRUSKAL.description}.\n"

        print(msg)
        method = UserInteraction.read_natural_number(len(UserInteraction.GeneratorAlgorithm))

        def get_algorithm_by_value(value) -> UserInteraction.GeneratorAlgorithm:
            for algorithm in UserInteraction.GeneratorAlgorithm:
                if algorithm.value == value:
                    return algorithm

        if method == UserInteraction.GeneratorAlgorithm.BACKTRACKING.value:
            msg = "\nВведите параметр генерации - строку и столбец стартовой клетки для запуска бэктрекинга"
            print(msg)
            start = UserInteraction.get_cell_coords(height, width)
            return get_algorithm_by_value(method), start

        return get_algorithm_by_value(method), None

    @staticmethod
    def read_solver_params(height: int, width: int) -> Tuple[SolverAlgorithm, Coordinate, Coordinate]:
        """
        Считывание метода решения лабиринта и координат стартовой и конечной клетки.

        Args:
            height (int): Высота лабиринта.
            width (int): Ширина лабиринта.

        Returns:
            Tuple[SolverAlgorithm, Coordinate, Coordinate]: Выбранный метод решения, координаты стартовой и
            конечной клеток.
        """

        UserInteraction.clear_console()
        msg = f"Выберите метод решения лабиринта: " \
              f"{UserInteraction.SolverAlgorithm.BACKTRACKING.value} - " \
              f"{UserInteraction.SolverAlgorithm.BACKTRACKING.description}, " \
              f"{UserInteraction.SolverAlgorithm.BFS.value} - " \
              f"{UserInteraction.SolverAlgorithm.BFS.description}.\n"

        print(msg)
        method = UserInteraction.read_natural_number(len(UserInteraction.SolverAlgorithm))

        def get_algorithm_by_value(value) -> UserInteraction.SolverAlgorithm:
            for algorithm in UserInteraction.SolverAlgorithm:
                if algorithm.value == value:
                    return algorithm

        msg = "\nВведите координаты стартовой клетки - строку и столбец."
        print(msg)
        start = UserInteraction.get_cell_coords(height, width)

        msg = "\nВведите координаты финишной клетки - строку и столбец."
        print(msg)
        finish = UserInteraction.get_cell_coords(height, width)

        return get_algorithm_by_value(method), start, finish

    @staticmethod
    def get_cell_coords(height_restr: int, width_restr: int) -> Coordinate:
        """
        Получение координат клетки в пределах указанных размеров лабиринта.

        Args:
            height_restr (int): Максимально допустимое значение строки.
            width_restr (int): Максимально допустимое значение столбца.

        Returns:
            Coordinate: Координаты клетки.
        """

        row = UserInteraction.read_natural_number(height_restr)
        col = UserInteraction.read_natural_number(width_restr)

        return Coordinate(row, col)

    @staticmethod
    def read_natural_number(max_restr: int = None) -> int:
        """
        Считывание натурального числа с опциональным ограничением сверху.

        Args:
            max_restr (Optional[int]): Максимально допустимое значение (если есть).

        Returns:
            int: Введённое натуральное число.
        """
        msg_restr = ""
        if max_restr is not None:
            msg_restr += f"Введите одно число от 1 до {max_restr}.\n"

        while True:
            print(msg_restr, end='')
            user_input = input().strip()

            if user_input.isdigit():
                number = int(user_input)
                if number == 0:
                    continue
                elif max_restr is not None and number > max_restr:
                    continue
                else:
                    return number
            else:
                print("Ошибка: введите только цифры без пробелов и других символов.")

    @staticmethod
    def clear_console() -> None:
        """
        Очистка консоли.

        Returns:
            None
        """
        os.system('cls' if os.name == 'nt' else 'clear')
