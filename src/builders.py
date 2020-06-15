from utils.database import db


class ServiceBuilder:

    def __init__(self, service_class):
        self.service_class = service_class

    def build(self):
        return self.service_class(db.connection)