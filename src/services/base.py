class BaseService:

    def __init__(self, connection):
        self.connection = connection


class ModelService(BaseService):
    model_class = None

    def __init__(self, connection):
        super().__init__(connection)
        self.model = self.model_class(self.connection)
