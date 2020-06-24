from flask.views import MethodView
from builders import ServiceBuilder


class ServiceView(MethodView):
    service_class = None

    def __init__(self):
        super().__init__()
        self.service = ServiceBuilder(self.service_class).build()


class SchemaView(MethodView):
    schema_class = None

    def __init__(self):
        super().__init__()
        self.schema = self.schema_class()

    def schema_response(self, data):
        return self.schema.dump(data)
