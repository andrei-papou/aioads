class Serializer:

    def __init__(self, result_proxy, schema, many=False):
        self.rp = result_proxy
        self.schema = schema
        self.many = many

    async def serialize(self):
        self.data = await self.rp.fetchall()
        serialized_data = []
        self._serialize_level(container=serialized_data, rows=self.data, schema=self.schema)
        return serialized_data

    def _get_row_hash(self, row, fields):
        return '___'.join(map(str, [v for k, v in row.items() if k in fields]))

    def _serialize_level(self, container, rows, schema):
        fields = []
        db_fields = []
        agr_fields = []

        # splitting fields into two sections: fields that should be populated on this level and fields that
        # aggregate data from the deeper level
        for db_name, json_name in schema.items():
            if type(json_name) is str:
                fields.append((db_name, json_name))
                db_fields.append(db_name)
            else:
                agr_fields.append(db_name)

        for row in rows:
            _row_hash = self._get_row_hash(row, db_fields)

            exists = False
            for i in container:
                if i['_row_hash'] == _row_hash and _row_hash != '':
                    exists = True

            if exists:
                continue

            item = {}

            for db_name, json_name in fields:
                item[json_name] = row[db_name]
            item['_row_hash'] = _row_hash

            for agr_f in agr_fields:
                item[agr_f] = []

            container.append(item)

        for item in container:
            for agr_f in agr_fields:
                agr_rows = []
                for row in rows:
                    if item['_row_hash'] == self._get_row_hash(row, db_fields):
                        agr_rows.append(row)
                self._serialize_level(item[agr_f], agr_rows, schema[agr_f])
            del item['_row_hash']


def serialize(schema, many=True):
    def decorator(method):
        async def wrapper(*args, **kwargs):
            result_proxy = await method(*args, **kwargs)
            serializer = Serializer(result_proxy=result_proxy, schema=schema, many=many)
            return await serializer.serialize()
        return wrapper
    return decorator
