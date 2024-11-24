from abc import abstractmethod, ABC
from enum import StrEnum
from typing import List

from src.coordinate import Coordinate
from src.maze import Maze


class IRenderer(ABC):
    @staticmethod
    @abstractmethod
    def render(maze: Maze, path: List[Coordinate]) -> List[List[str]]:
        """
        Отрисовывает лабиринт в консоль и отображет заданный путь в лабиринте.

        Args:
            maze (Maze): Лабиринт, который нужно отобразить.
            path (Optional[List[Coordinate]]): Список координат, представляющих путь,
                который будет отображен. Если путь не указан, отображается только лабиринт.

        Returns:
            List[List[str]]: Двумерный список симфолов Unicode, представляющий лабиринт с возможным маршрутом.
        """
        pass


class ConsoleRenderer(IRenderer):
    class Border(StrEnum):
        HORIZONTAL_LINE = '─'
        VERTICAL_LINE = '│'
        SPACE = ' '
        
    class CellContent(StrEnum):
        START = 'S'
        FINISH = 'F'
        ROUTE_USUAL_CELL = '*'

    borders = [' ', '╴', '╷', '┐', '╶', '─', '┌', '┬', '╵', '┘', '│', '┤', '└', '┴', '├', '┼']
    right_borders = ['╶', '─', '┌', '┬', '└', '┴', '├', '┼']
    upper_borders = ['╵', '└', '┘', '┴', '│', '├', '┤', '┼']
    lower_borders = ['╷', '┌', '┐', '┬', '│', '├', '┤', '┼']

    @staticmethod
    def render(maze: Maze, path: List[Coordinate] = None) -> List[List[str]]:
        """
        Генерирует компактное представление лабиринта, пропорционально расширяет его по вергикали и горизонтали
        так чтобы стало достаточно места для отображения пути и отображает заданный путь.

        Args:
            maze (Maze): Лабиринт, который нужно отобразить.
            path (Optional[List[Coordinate]]): Список координат, представляющих путь.
                Если путь не передан, отобразится только лабиринт.

        Returns:
            List[List[str]]: Двумерный список символов Unicode, представляющий лабиринт с заданным маршрутом.
        """

        if path is None:
            path = []

        tiny_repr = ConsoleRenderer.render_tiny(maze)
        expanded_horizontally_repr = ConsoleRenderer.expand_horizontally(tiny_repr)
        full_repr = ConsoleRenderer.expand_vertically(expanded_horizontally_repr)

        full_repr_with_path = ConsoleRenderer.render_path(full_repr, path)

        return full_repr_with_path

    @staticmethod
    def render_tiny(maze: Maze) -> List[List[str]]:
        """
        Отрисовывает компактную версию лабиринта (без достаточного количества места для отобраджения маршрутов).

        Args:
            maze (Maze): Лабиринт, который нужно отобразить.

        Returns:
            List[List[str]]: Компактное представление лабиринта.
        """
        tiny_repr = []

        for x in range(1, maze.height + 2):
            tiny_repr.append([])
            for y in range(1, maze.width + 2):
                upper = maze.get_cell(Coordinate(x - 1, y)).left_wall
                right = maze.get_cell(Coordinate(x, y)).upper_wall
                lower = maze.get_cell(Coordinate(x, y)).left_wall
                left = maze.get_cell(Coordinate(x, y - 1)).upper_wall

                char = (upper << 3) + (right << 2) + (lower << 1) + left
                tiny_repr[-1].append(ConsoleRenderer.borders[char])

                if right == 0:
                    if y < maze.width + 1:
                        tiny_repr[-1].append(ConsoleRenderer.Border.SPACE)
                else:
                    tiny_repr[-1].append(ConsoleRenderer.Border.HORIZONTAL_LINE)

        return tiny_repr

    @staticmethod
    def render_path(full_repr: List[List[str]], path: List[Coordinate] = None) -> List[List[str]]:
        """
        Принимает полное отображение лабиринта (полное отображение - это компактное отображение, которое было растянуто
        1 раз по вертикали и 1 раз по горизонтали) и добавляет заданный маршрут в отображение лабиринта.

        Args:
            full_repr (List[List[str]]): Полное представление лабиринта (без пути).
            path (Optional[List[Coordinate]]): Список координат, представляющий маршрут.

        Returns:
            List[List[str]]: Двумерное представление лабиринта с маршрутом.
        """

        def set_cell_content_in_full_repr(_full_repr: List[List[str]], _coord: Coordinate, char: str) -> None:
            """
            Устанавливает содержимое клетки в полном представлении лабиринта.

            Args:
                _full_repr (List[List[str]]): Полное представление лабиринта.
                _coord (Coordinate): Координаты ячейки, в которую нужно поместить символ.
                char (str): Символ для отображения в ячейке.
            """
            _full_repr[(_coord.row - 1) * 2 + 1][(_coord.col - 1) * 4 + 2] = char

        if len(path) < 2:
            return full_repr

        full_repr_with_path = [row[:] for row in full_repr]

        for coord in path[1:-1]:
            set_cell_content_in_full_repr(full_repr_with_path, coord, ConsoleRenderer.CellContent.ROUTE_USUAL_CELL)

        set_cell_content_in_full_repr(full_repr_with_path, path[0], ConsoleRenderer.CellContent.START)
        set_cell_content_in_full_repr(full_repr_with_path, path[-1], ConsoleRenderer.CellContent.FINISH)

        return full_repr_with_path

    @staticmethod
    def expand_horizontally(narrow_repr: List[List[str]]) -> List[List[str]]:
        """
        Растягивает лабиринт по горизонтали посредством добавления горизонтальной стены или побела после
        каждого символа в каждой строке исходного представления.

        Args:
            narrow_repr (List[List[str]]): Исходное представление лабиринта.

        Returns:
            List[List[str]]: Растянутое по горизонтали представление лабиринта.
        """
        wide_repr = []
        for x in range(len(narrow_repr)):
            wide_repr.append([])
            for y in range(len(narrow_repr[x])-1):
                char = narrow_repr[x][y]
                wide_repr[-1].append(char)
                if char in list(set(ConsoleRenderer.borders) - set(ConsoleRenderer.right_borders)):
                    wide_repr[-1].append(ConsoleRenderer.Border.SPACE)
                else:
                    wide_repr[-1].append(ConsoleRenderer.Border.HORIZONTAL_LINE)
            wide_repr[-1].append(narrow_repr[x][-1])

        return wide_repr

    @staticmethod
    def expand_vertically(low_repr: List[List[str]]) -> List[List[str]]:
        """
        Растягивает лабиринт по вертикали посредством добавления строки с вертикальными стенами и побелами после
        каждоой строки исходного представления.

        Args:
            low_repr (List[List[str]]): Исходное представление лабиринта.

        Returns:
            List[List[str]]: Растяутое по вертикали представление лабиринта.
        """
        high_repr = []
        for x in range(len(low_repr) - 1):
            high_repr.append(low_repr[x].copy())
            high_repr.append([' '] * len(high_repr[-1]))

            for j in range(len(low_repr[x])):
                if high_repr[-2][j] in ConsoleRenderer.lower_borders or \
                        low_repr[x + 1][j] in ConsoleRenderer.upper_borders:
                    high_repr[-1][j] = ConsoleRenderer.Border.VERTICAL_LINE
                else:
                    if j > 0 and high_repr[-2][j - 1] == ' ' and \
                            j + 1 < len(high_repr[-1]) and high_repr[-2][j + 1] != '│':
                        high_repr[-1][j] = ConsoleRenderer.Border.SPACE

        high_repr.append(low_repr[-1].copy())
        return high_repr

    @staticmethod
    def print_to_console(maze: Maze, path: List[Coordinate] = None) -> None:
        """
        Печатает лабиринт с заданным маршрутом в консоль.

        Args:
            maze (Maze): Лабиринт, который нужно напечатать.
            path (Optional[List[Coordinate]]): Путь, который нужно отобразить, если передан.
        """
        output = ConsoleRenderer.render(maze, path)
        [print(''.join(output[i])) for i in range(len(output))]
