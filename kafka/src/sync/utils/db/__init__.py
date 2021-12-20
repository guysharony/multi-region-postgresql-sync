# -*- coding: utf-8 -*-
import os
from typing import Any
from typing import Optional

from utils.format import as_list_of_string
from utils.db.result import Result
from utils.db.result.keys import Keys
from utils.db.returning import Returning
from utils.db.connection import Connection


class DB:
    def __init__(self, prefix: str = 'SOURCE') -> None:
        self._statements = {
            'select': {
                'operations': [
                    'where',
                    'returning',
                    'order by',
                    'limit',
                    'inner join',
                    'full join']
            },
            'insert': {
                'operations': ['returning']
            },
            'update': {
                'operations': ['where', 'returning']
            },
            'delete': {
                'operations': ['where', 'returning']
            }
        }

        self._fetch = False
        self._commit = False
        self._statement = None
        self._last_operation = None

        self._connection = Connection(
                            user=os.environ[prefix + '_DB_USER'],
                            password=os.environ[prefix + '_DB_PASSWORD'],
                            host=os.environ[prefix + '_DB_HOST'],
                            port=os.environ[prefix + '_DB_PORT'],
                            database=os.environ[prefix + '_DB_NAME'])

        self._returning = Returning()
        self._tables = Keys()
        self._where = Keys()
        self._inner_join = None
        self._full_join = None
        self._order_by = None
        self._limit = None

        self._where.join = ' AND '

    def __del__(self):
        self._fetch = False
        self._commit = False
        self._statement = None
        self._last_operation = None
        self._connection.close()
        self._returning.__del__()
        self._tables.__del__()

        self._where.__del__()
        self._inner_join = None
        self._full_join = None
        self._order_by = None
        self._limit = None

        self._where.join = ' AND '

    @property
    def query(self):
        self.set_query_statement()
        return self._connection.query

    @query.setter
    def query(self, value: str = None):
        self._connection.query = value

    @property
    def length(self) -> int:
        return self._returning.length

    @property
    def items(self):
        return self._returning.items

    @property
    def first(self) -> Optional[Any]:
        return self.get(0)

    @property
    def exists(self) -> bool:
        return self.length > 0

    @property
    def last(self) -> Optional[Any]:
        return self.get(self.length - 1) if self.length > 0 else None

    def get(self, index: int) -> Optional[Any]:
        if index >= self.length or self.items is None:
            return None

        return self.items[index]

    def select(self, tables):
        self.set_statement('select')
        self.set_tables(tables)

        return self

    def insert(self, table: str, keys: list):
        self.set_statement('insert')
        self.set_tables(table)

        self._commit = True

        st_keys = Keys().stringify(keys)
        st_values = Keys().stringify(['%s'] * len(keys))

        query = 'INSERT INTO '
        query += str(self._tables)
        query += " (" + st_keys + ") VALUES (" + st_values + ")"
        self._connection.query = query

        return self

    def update(self, table: str, set: list):
        self.set_statement('update')
        self.set_tables(table)

        self._commit = True

        query = 'UPDATE '
        query += str(self._tables)
        query += ' SET '

        for key, value in enumerate(set):
            if isinstance(value, dict):
                for k, v in value.items():
                    query += (', ' if key else '') + k + " = " + v
            else:
                query += (', ' if key else '') + value + " = %s"

        self._connection.query = query

        return self

    def delete(self, table: str):
        self.set_statement('delete')
        self.set_tables(table)

        self._commit = True

        query = 'DELETE FROM '
        query += str(self._tables)

        self._connection.query = query

        return self

    def where(self, conditions):
        self.is_operation_allowed('where')
        self._where.items = self._where.items + as_list_of_string(conditions)
        self.set_query_operation('where')

        return self

    def order_by(self, conditions):
        self.is_operation_allowed('order by')

        self._order_by = conditions

        self.set_query_operation('order by')

        return self

    def limit(self, conditions):
        self.is_operation_allowed('limit')

        self._limit = str(conditions)

        self.set_query_operation('limit')

        return self

    def inner_join(self, tables, conditions: str):
        self.is_operation_allowed('inner join')

        st_tables = ', '.join(as_list_of_string(tables))
        st_condition = ' ON ' + str(conditions)

        self._inner_join = st_tables + st_condition

        self.set_query_operation('inner join')

        return self

    def full_join(self, tables, conditions: str):
        self.is_operation_allowed('full join')

        st_tables = ', '.join(as_list_of_string(tables))
        st_condition = ' ON ' + str(conditions)

        self._full_join = st_tables + st_condition

        self.set_query_operation('full join')

        return self

    def returning(self, values: list, replace_by: list = None):
        self._returning = Returning(as_list_of_string(values), replace_by)

        if self._statement is None:
            raise IndexError('Statement not defined.')

        self._statement['used'].append('returning')

        return self

    def execute(self, values: list = None):
        self.set_query_statement()

        self._connection.open()
        self._connection.execute(values)
        self._returning.columns = self._connection.columns
        self.set_result(self._connection.fetchall() if self._fetch else None)

        if self._commit:
            self._connection.commit()

        return self

    def set_statement(self, statement):
        if self._statement:
            self.__del__()

        if statement not in self._statements:
            raise IndexError(f"'{statement}' statement is not defined.")

        self._statement = self._statements[statement]
        self._statement['key'] = statement
        self._statement['used'] = []

    def set_tables(self, tables):
        if self._tables and self._tables.length:
            raise IndexError('Tables are already selected.')

        self._tables.items = as_list_of_string(tables)

    def set_query_operation(self, operation: str):
        if self._connection.query is None:
            self._connection.query = ''

        if operation == 'where':
            self.set_last_operation(
                'where',
                str(self._where))

        if operation == 'inner join' \
                and self._inner_join:
            self.set_last_operation(
                'inner join',
                self._inner_join)

        if operation == 'full join' \
                and self._full_join:
            self.set_last_operation(
                'full join',
                self._full_join)

        if operation == 'order by' \
                and self._order_by:
            self.set_last_operation(
                'order by',
                self._order_by)

        if operation == 'limit' \
                and self._limit:
            self.set_last_operation(
                'limit',
                self._limit)

    def set_last_operation(self, operation: str, query: str):
        if self._statement is None:
            raise IndexError('Statement not defined.')

        if self._last_operation:
            oper = self._last_operation['operation']

            if oper == operation:
                self._last_operation['query'] = query
                return

            self.append_operation()

        self._statement['used'].append(operation)

        self._last_operation = {
            'operation': operation,
            'query': query
        }

    def append_operation(self):
        if self._last_operation:
            operation = self._last_operation['operation']
            query = self._last_operation['query']

            if self._connection.query is None:
                self._connection.query = ''

            if self._statement is None:
                raise IndexError('Statement not defined.')

            if operation == 'where':
                self._connection.query += ' WHERE '
            if operation == 'order by':
                self._connection.query += ' ORDER BY '
            if operation == 'inner join':
                self._connection.query += ' INNER JOIN '
            if operation == 'full join':
                self._connection.query += ' FULL JOIN '
            if operation == 'limit':
                self._connection.query += ' LIMIT '

            self._connection.query += query

    def set_query_statement(self):
        if self._statement and 'key' in self._statement:
            statement = self._statement['key']

            if statement == 'select':
                self.append_operation()

                st_keys = str(self._returning.expected_keys)
                verify_keys = self._returning.expected_length

                query = 'SELECT '
                query += st_keys if verify_keys else '*'
                query += ' FROM '
                query += str(self._tables)

                conn_query = self._connection.query
                old_qury = conn_query if conn_query else ''

                self.query = query + old_qury + ';'
                self._fetch = True

            elif self._connection.query and statement == 'insert':
                if self._returning.expected_length > 0:
                    st_keys = str(self._returning.expected_keys)

                    self._fetch = True
                    self._connection.query += f" RETURNING {st_keys}"

                self._connection.query += ";"

            elif self._connection.query and statement == 'update':
                self.append_operation()

                if self._returning.expected_length > 0:
                    st_keys = str(self._returning.expected_keys)

                    self._fetch = True
                    self._connection.query += f" RETURNING {st_keys}"

                self._connection.query += ";"

            elif self._connection.query and statement == 'delete':
                self.append_operation()

                if self._returning.expected_length > 0:
                    st_keys = str(self._returning.expected_keys)

                    self._fetch = True
                    self._connection.query += f" RETURNING {st_keys}"

                self._connection.query += ";"

            else:
                raise IndexError(f"'{statement}' statement is not defined.")

    def set_result(self, values: list = None):
        if values is None:
            return self._returning.__del__()

        if values:
            for value in values:
                if self._returning.columns \
                        and (len(self._returning.columns) != len(value)):
                    return self._returning.__del__()

                self._returning.append(Result(self._returning.columns, value))

    def is_operation_allowed(self, operation):
        if self._statement is None:
            raise IndexError('Statement is not defined.')

        if operation not in self._statement['operations']:
            raise IndexError(f"'{operation}' operation is not allowed.")

        common = None

        if operation == 'where':
            common = self.is_used([
                'limit',
                'order by',
                'returning'])

        if operation == 'inner join':
            common = self.is_used([
                'where',
                'inner join',
                'full join',
                'limit',
                'order by',
                'returning'])

        if operation == 'full join':
            common = self.is_used([
                'where',
                'inner join',
                'full join',
                'limit',
                'order by',
                'returning'])

        if operation == 'order by':
            common = self.is_used([
                'order by'])

        if operation == 'limit':
            common = self.is_used([
                'limit'])

        if common:
            old_oper = ', '.join(common)
            raise IndexError(f"'{operation}' not allowed after '{old_oper}'")

    def is_used(self, forbiden: list):
        if self._statement is None:
            raise IndexError('Statement is not defined.')

        return set(forbiden) & set(self._statement['used'])
