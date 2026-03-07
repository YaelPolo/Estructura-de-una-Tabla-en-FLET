class ApiError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def api_error_to_text(error: ApiError):
    return str(error.message)