class BaseService:

    def __init__(self, connection):
        self.connection = connection


class ModelService(BaseService):
    model_class = None

    def __init__(self, connection):
        super().__init__(connection)
        self.model = self.model_class(self.connection)


class SchemaService(BaseService):
    schema_class = None

    def __init__(self, connection):
        super().__init__(connection)
        self.schema = self.schema_class()

    def to_response(self, data):
        return self.schema.dump(data)
