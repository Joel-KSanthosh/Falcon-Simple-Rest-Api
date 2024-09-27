from typing_extensions import override


class MessageResponse:
    def __init__(self, message):
        self.message = message

    def response(self):
        return {
            "message" : self.message,
        }


class CustomResponse(MessageResponse):
    def __init__(self, message, data):
        super().__init__(message)
        self.data = data

    @override
    def response(self):
        return {
            "message" : self.message,
            "data" : self.data
        }