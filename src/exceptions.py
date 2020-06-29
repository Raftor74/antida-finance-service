class ServiceError(Exception):
    service = None

    def __init__(self, *args, field_name: str = "", field_error: str = ""):
        super().__init__(self.service, *args)
        self._field_name = field_name
        self._field_error = field_error

    def get_error_message(self):
        return {self._field_name: self._field_error}
