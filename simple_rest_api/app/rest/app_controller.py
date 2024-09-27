from custom_response import MessageResponse, CustomResponse
from service.user_service import UserService
from logger import logger


class UserGet:
    def __init__(self):
        self.service = UserService()


    def on_get(self,req,resp,email=None): # noqa
        result = self.service.find(email)
        if result:
            resp.media = CustomResponse(message = "Successfully Fetched User",data = result).response()
        else:
            resp.media = MessageResponse(message = "User not found").response()



class UserPost:
    def __init__(self):
        self.service = UserService()

    def on_post(self,req,resp): # noqa
        body : dict = req.media
        email = self.service.create(body)
        resp.media = MessageResponse(f"User created successfully : {email}").response()

class ExceptionHandler:
    def custom_exception_handler(self,req,resp,ex,params): # noqa
        resp.status = ex.status
        resp.media = MessageResponse(ex.error).response()
        logger.error(ex.error)




