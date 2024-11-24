class Cell:
    def __init__(self, left_wall: bool, upper_wall: bool, captured: bool):
        """
        Инициализация ячейки.

        Args:
            left_wall (bool): Наличие левой стены.
            upper_wall (bool): Наличие верхней стены.
            captured (bool): Флаг принимает значение True, если ячейка заблокирована и False, иначе.
        """
        self._left_wall = left_wall
        self._upper_wall = upper_wall
        self._captured = captured

    @property
    def left_wall(self) -> bool:
        """
        Возвращает наличие левой стены.

        Returns:
            bool: True, если левая стена присутствует, иначе False.
        """
        return self._left_wall

    @left_wall.setter
    def left_wall(self, left_wall: bool) -> None:
        """
        Устанавливает наличие левой стены.

        Args:
            value (bool): True для установки стены, False для удаления.
        """
        self._left_wall = left_wall

    @property
    def upper_wall(self) -> bool:
        """
        Возвращает наличие верхней стены.

        Returns:
            bool: True, если верхняя стена присутствует, иначе False.
        """
        return self._upper_wall

    @upper_wall.setter
    def upper_wall(self, upper_wall: bool) -> None:
        """
        Устанавливает наличие верхней стены.

        Args:
            value (bool): True для установки стены, False для удаления.
        """
        self._upper_wall = upper_wall

    @property
    def captured(self) -> bool:
        """
        Возвращает флаг - заблкирована ли ячейка.

        Returns:
            bool: True, если ячейка заблокирована, иначе False.
        """
        return self._captured

    @captured.setter
    def captured(self, captured: bool) -> None:
        """
        Устанавливает флаг - заблкирована ли ячейка.

        Args:
            value (bool): True если ячейка заблокирована, иначе False.
        """
        self._captured = captured
