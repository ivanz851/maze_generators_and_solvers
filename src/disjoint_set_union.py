class DisjointSetUnion:
    """
    Реализация системы непересекающихся множеств с эвристикой сжатия путей и ранговой эвристикой.
    Обеспечивает почти константное время работы O(a(n)) на запрос, где n - размер системы,
    a - обратная функция Аккермана.
    """
    def __init__(self, elements: int):
        """
        Инициализация системы непересекающихся множеств.

        Args:
            elements (int): Количество элементов в системе.
        """
        self._parent = [None] * elements
        self._rank = [None] * elements

        for i in range(elements):
            self.init_set(i)

    def init_set(self, v: int) -> None:
        """
        Добавляет новый элемент v, помещая его в новое множество, состоящее из одного него.

        Args:
            v (int): Индекс элемента.
        """
        self._parent[v] = v
        self._rank[v] = 0

    def get_set(self, v: int) -> int:
        """
        Находит лидера множества, которому принадлежит элемент.

        Args:
            v (int): Элемент, для которого ищется лидер множества.

        Returns:
            int: Лидер множества.
        """
        if v == self._parent[v]:
            return v

        self._parent[v] = self.get_set(self._parent[v])
        return self._parent[v]

    def unite_sets(self, v: int, u: int) -> None:
        """
        Объединяет два указанных множества (множество, в котором находится элемент v,
        и множество, в котором находится элемент u)

        Args:
            v (int): Первый элемент.
            u (int): Второй элемент.
        """
        v = self.get_set(v)
        u = self.get_set(u)

        if v != u:
            if self._rank[v] < self._rank[u]:
                v, u = u, v

            self._parent[u] = v
            if self._rank[v] == self._rank[u]:
                self._rank[v] += 1
