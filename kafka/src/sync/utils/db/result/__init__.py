class Result:
    def __init__(self, keys: list = None, values: list = None):
        self._keys = []
        self._values = []

        self._length = 0
        self._items = {}

        self._setkeys(keys)
        self._setvalues(values)

        self._setitems()

    @property
    def __dict__(self) -> dict:
        return self._items

    def __getitem__(self, key: str):
        return self.get(key)

    @property
    def keys(self) -> list:
        return self._keys

    @property
    def values(self) -> list:
        return self._values

    @property
    def length(self) -> int:
        return self._length

    def exists(self, key: str):
        return key in self._items

    def append(self, key: str, value):
        exists = self.exists(key)

        self._items[key] = value

        if not exists:
            self._length = self._length + 1

    def get(self, key: str):
        return self._items[key] if self.exists(key) else None

    def pop(self, key: str):
        if self.exists(key):
            self._items.pop(key)

    def _setkeys(self, keys: list = None):
        if keys:
            self._keys = keys

    def _setvalues(self, values: list = None):
        if values:
            self._values = values

    def _getvalues(self, index: int = None):
        if index is None:
            return self._values

        if index < 0:
            raise IndexError('Index out of range.')

        return self._values[index] if index <= len(self._values) else None

    def _setitems(self):
        for key, value in enumerate(self._keys):
            self.append(value, self._getvalues(key))
