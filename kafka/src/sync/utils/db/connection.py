import psycopg2


class Connection:
    def __init__(self, **kwargs):
        self._conn = kwargs

        self._connect = None
        self._cursor = None
        self._query = None
        self._columns = None

    def __del__(self):
        self.close()
        self._connect = None
        self._cursor = None

    def open(self):
        self._connect = psycopg2.connect(**self._conn)
        self._connect.set_client_encoding('UTF-8')
        self._cursor = self._connect.cursor()

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: str = None):
        self._query = value

    @property
    def columns(self):
        return self._columns

    def close(self):
        self._query = None
        self._columns = None

        if self._connect:
            self._connect.close()

        if self._cursor:
            self._cursor.close()

    def commit(self):
        if self._connect:
            self._connect.commit()

    def execute(self, values: list = None):
        if self._cursor:
            self._cursor.execute(self.query, values)
            if self._cursor.description:
                self._columns = [desc[0] for desc in self._cursor.description]

    def fetchall(self):
        return self._cursor.fetchall() if self._cursor else None
