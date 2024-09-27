from falcon.status_codes import HTTP_400


class CustomException(Exception):
    def __init__(self,message,status_code=HTTP_400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


