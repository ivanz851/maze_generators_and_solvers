from src.cell import Cell
from src.coordinate import Coordinate


class Maze:
    def __init__(self, height: int, width: int, walls_inside: bool = True):
        """
        Инициализирует лабиринт с заданной высотой и шириной (измеряется в Cells).
        По умолчанию walls_inside = True, т.е. внутри лабиринта заданы все стены,
        чтобы генератор мог убирать ненужные для создания проходов.
        walls_inside = False, если необходимо чтобы внутри лабиринта не было стен (например, для генерации лабиринта
        вручную написании тестов)

        Args:
            height (int): Высота внутренней области лабиринта.
            width (int): Ширина внутренней области лабиринта.
        """
        self._height = height
        self._width = width
        self._map_height = height + 2
        self._map_width = width + 2
        self._map = None
        self.init_map(walls_inside)

    def init_map(self, walls_inside: bool) -> None:
        """
        Инициализирует карту лабиринта с ячейками. Карта устроена так, что с каждой стороны есь полоска вспомогательных
        клеток, которые изначально помечаются заблокированными, чтобы при обходе рабочей части лабиринта не обрабатывать
        выходы за границы.
        """
        def create_cell(left_wall=False, upper_wall=False, captured=False) -> Cell:
            return Cell(left_wall=left_wall, upper_wall=upper_wall, captured=captured)

        self._map = [[create_cell(left_wall=walls_inside, upper_wall=walls_inside)
                      for _ in range(self._map_width)] for _ in range(self._map_height)]

        for x in range(self._map_height):
            self.set_cell(Coordinate(x, 0), create_cell(captured=True))
            self.set_cell(Coordinate(x, self._map_width - 1), create_cell(left_wall=True, captured=True))

        for y in range(self._map_width):
            self.set_cell(Coordinate(0, y), create_cell(captured=True))
            self.set_cell(Coordinate(self._map_height - 1, y), create_cell(upper_wall=True, captured=True))

        self.set_cell(Coordinate(self._map_height - 1, 0), create_cell(captured=True))
        self.set_cell(Coordinate(self._map_height - 1, self._map_width - 1), create_cell(captured=True))

    @property
    def height(self) -> int:
        """
        Возвращает высоту рабочей части лабиринта.

        Returns:
            int: Высота рабочей части лабиринта.
        """
        return self._height

    @property
    def width(self) -> int:
        """
        Возвращает ширину рабочей части лабиринта.

        Returns:
            int: Ширина рабочей части лабиринта.
        """
        return self._width

    @property
    def map_height(self) -> int:
        """
        Возвращает полную высоту лабиринта, включая границы.

        Returns:
            int: Высота всей карты лабиринта.
        """
        return self._map_height

    @property
    def map_width(self) -> int:
        """
        Возвращает полную ширину карты лабиринта, включая границы.

        Returns:
            int: Ширина всей карты лабиринта.
        """
        return self._map_width

    def coordinate_inside_map(self, coordinate: Coordinate, consider_auxiliary_area: bool = False) -> bool:
        """
        Проверяет, находятся ли заданные координаты внутри карты лабиринта.

        Args:
            coordinate (Coordinate): Проверяемая координата.
            consider_auxiliary_area (bool): Учитывать ли вспомогательные границы карты (True - если их учитывать,
            False, если рассматривается только рабочая часть карты).

        Returns:
            bool: True, если заданные координаты находятся внутри карты, иначе False.
        """
        if consider_auxiliary_area:
            return True if 0 <= coordinate.row < self._map_height and 0 <= coordinate.col < self._map_width else False
        else:
            return True if 1 <= coordinate.row < self._map_height - 1 and \
                           1 <= coordinate.col < self._map_width - 1 else False

    def get_cell(self, coordinate: Coordinate) -> Cell:
        """
        Возвращает ячейку по заданным координатам.

        Args:
            coordinate (Coordinate): Координаты ячейки.

        Returns:
            Cell: Ячейка с заданными координатами.
        """
        if self.coordinate_inside_map(coordinate, consider_auxiliary_area=True):
            return self._map[coordinate.row][coordinate.col]

    def set_cell(self, coordinate: Coordinate, cell: Cell) -> None:
        """
        Устанавливает заданную ячейку по заданным координатам.

        Args:
            coordinate (Coordinate): Координаты ячейки.
            cell (Cell): Новая ячейка для установки.
        """
        if self.coordinate_inside_map(coordinate, consider_auxiliary_area=True):
            self._map[coordinate.row][coordinate.col] = cell

    def update_cell(self, coordinate: Coordinate, left_wall: bool = None, upper_wall: bool = None,
                    captured: bool = None) -> None:
        """
       Обновляет свойства ячейки с заданными координатами.

       Args:
           coordinate (Coordinate): Координата ячейки.
           left_wall (bool, optional): Обновление наличия левой стены.
           upper_wall (bool, optional): Обновление наличия верхней стены.
           captured (bool, optional): Обновление флага блокировки.
       """
        if not self.coordinate_inside_map(coordinate, consider_auxiliary_area=True):
            return

        cell = self.get_cell(coordinate)
        if left_wall is not None:
            cell._left_wall = left_wall
        if upper_wall is not None:
            cell._upper_wall = upper_wall
        if captured is not None:
            cell._captured = captured

    def check_wall(self, cur: Coordinate, neighbor: Coordinate) -> bool:
        """
        Проверяет, есть ли стена между двумя соседними ячейками.

        Args:
            cur (Coordinate): Текущая ячейка.
            neighbor (Coordinate): Соседняя ячейка.

        Returns:
            bool: True, если между ячейками есть стена, иначе False.
        """
        if neighbor.row < cur.row:
            return self.get_cell(cur).upper_wall
        if neighbor.row > cur.row:
            return self.get_cell(neighbor).upper_wall
        if neighbor.col < cur.col:
            return self.get_cell(cur).left_wall
        if neighbor.col > cur.col:
            return self.get_cell(neighbor).left_wall

    def reset_captured(self) -> None:
        """
        Сбрасывает флаг блокировки для всех ячеек рабочей части карты.
        """
        for i in range(1, self._map_height - 1):
            for j in range(1, self._map_width - 1):
                self.update_cell(Coordinate(i, j), captured=False)
