from falcon.status_codes import HTTP_500

from falcon.http_error import HTTPError
from typing_extensions import override


class CustomException(HTTPError):
    def __init__(self, resp_json='Internal Server Error', status=HTTP_500):
        super().__init__(status)
        self.error = resp_json
        self.status = status

    @override
    def to_dict(self, obj_type=dict):
        super().to_dict(obj_type)
        return self.error


class DatabaseCorruptedException(CustomException):
    pass


class EmailAlreadyExistException(CustomException):
    pass


class ValidationException(CustomException):
    pass


class UserNotFoundException(CustomException):
    pass

