class CustomResponse:
    def __init__(self,message,data=None):
        self.message = message
        self.data = data

    def response(self):
        if self.data is None:
            return {
                "message": self.message
            }
        else:
            return {
                "message" : self.message,
                "data" : self.data
            }
