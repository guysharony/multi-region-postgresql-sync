class Keys:
    def __init__(self, keys: list = None):
        self._items = keys if keys else []
        self._length = len(self._items)
        self._join = ', '
        self._repr = None

    def __del__(self):
        self._items = []
        self._length = 0
        self._join = ', '
        self._repr = None

    def __str__(self) -> str:
        return self.stringify(self._items)

    def stringify(self, keys: list) -> str:
        return self._join.join(keys)

    @property
    def join(self):
        return self._join

    @join.setter
    def join(self, value):
        self._join = str(value)

    @property
    def items(self) -> list:
        return self._items

    @items.setter
    def items(self, value: list):
        self._items = value

    @property
    def length(self) -> int:
        return self._length

    def append(self, keys: list):
        self._items.append(keys)
        self._length = len(self._items)
