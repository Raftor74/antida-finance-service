class QueryBuilder:
    table_name = None

    def __init__(self):
        self._select = ['*']
        self._table_name = self.table_name
        self._filter_placeholders = []
        self._filter_values = []
        self._limit = None
        self._offset = None
        self._order_by = None
        self._order_dir = None

    def reset(self):
        self._select = ['*']
        self._table_name = self.table_name
        self._filter_placeholders = []
        self._filter_values = []
        self._limit = None
        self._offset = None
        self._order_by = None
        self._order_dir = None
        return self

    def select(self, fields: list):
        self._select = fields
        return self

    def from_table(self, table_name: str):
        self._table_name = table_name
        return self

    def where(self, key: str, value, condition: str = '='):
        placeholder = self._build_filter_placeholder(key, condition)
        self._filter_placeholders.append(placeholder)
        self._filter_values.append(value)
        return self

    def where_raw(self, key: str, value, condition: str = '='):
        placeholder = f'{key} {condition} {value}'
        self._filter_placeholders.append(placeholder)
        return self

    def limit(self, limit: int):
        self._limit = limit
        return self

    def offset(self, offset: int):
        self._offset = offset
        return self

    def order(self, by: str, order: str = 'ASC'):
        self._order_by = by
        self._order_dir = order
        return self

    def build(self):
        select = self._build_select()
        table_from = self._build_table_from()
        where = self._build_filter()
        order = self._build_order()
        limit = self._build_limit()
        offset = self._build_offset()
        query = self._build_query(
            select, table_from, where, order, limit, offset
        ).strip()
        values = self._filter_values
        self.reset()
        return query, tuple(values)

    @classmethod
    def _build_filter_placeholder(cls, key: str, condition: str):
        return f'{key} {condition} ?'

    def _build_select(self):
        placeholder = ','.join(self._select)
        return f'SELECT {placeholder}'

    def _build_table_from(self):
        return f'FROM `{self._table_name}`'

    def _build_filter(self):
        placeholder = ' AND '.join(self._filter_placeholders)
        return f'WHERE {placeholder}'

    def _build_limit(self):
        if self._limit is not None:
            return f'LIMIT {self._limit}'
        return ''

    def _build_offset(self):
        if self._offset is not None:
            return f'OFFSET {self._offset}'
        return ''

    def _build_order(self):
        if self._order_by is not None:
            return f'ORDER BY {self._order_by} {self._order_dir}'
        return ''

    @classmethod
    def _build_query(cls, *args):
        return ' '.join(args)
