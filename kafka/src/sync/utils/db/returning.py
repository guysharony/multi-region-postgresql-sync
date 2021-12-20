from utils.db.result import Result
from utils.db.result.keys import Keys


class Returning:
    def __init__(self, expected_keys: list = None, replace_by: list = None):
        self._items = None
        self._length = 0
        self._columns = None
        self._replace_by = Keys(replace_by if replace_by else expected_keys)
        self._expected_keys = Keys(expected_keys)

    def __del__(self):
        self._items = None
        self._length = 0
        self._expected_keys.__del__()

    def __getitem__(self, key):
        if self._items is None:
            return None
        return self._items[key]

    @property
    def length(self) -> int:
        return self._length

    @property
    def items(self):
        return self._items

    @property
    def expected_length(self) -> int:
        return self._expected_keys.length

    @property
    def expected_keys(self) -> Keys:
        return self._expected_keys

    @property
    def indexed_by(self) -> Keys:
        return self._replace_by

    @indexed_by.setter
    def indexed_by(self, values):
        self._replace_by.items = values

    @property
    def columns(self):
        if self.indexed_by.length:
            return self.indexed_by.items

        return self._columns

    @columns.setter
    def columns(self, values):
        if values:
            indexed_length = self.indexed_by.length

            if indexed_length and (indexed_length != len(values)):
                raise IndexError("Expected columns length don't match.")

            self._columns = values

    def append_expected(self, keys: list):
        self._expected_keys.append(keys)

    def append(self, item: Result):
        if self._items is None:
            self._items = []

        self._items.append(vars(item))
        self._length = self._length + 1
