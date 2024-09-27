import json

from falcon.status_codes import HTTP_200, HTTP_400, HTTP_500

from simple_rest_api.app.custom_response import CustomResponse
from simple_rest_api.app.exception.exception import CustomException
from simple_rest_api.app.models.user import User


class AppController:
    def on_get(self,req,resp,email=None): # noqa
        if email:
            user = User.find_user_with_email(email)
            if user:
                resp.media = CustomResponse(message='Successfully Fetched.', data=user).response()
                resp.status = HTTP_200
            else:
                resp.media = CustomResponse(message="User with given email doesn't exist!").response()
                resp.status = HTTP_400
        else:
            user = list(User.find_all_user())
            if user:
                resp.media = CustomResponse(message='Successfully Fetched.', data=user).response()
            else:
                resp.media = CustomResponse(message="No users exist!").response()
                resp.status = HTTP_400

    def on_post(self,req,resp): # noqa
        body : dict = req.media

        required_fields = ['name','email','age']

        if len(body.keys()) != 3:
            raise CustomException("Request body is invalid!")

        user = User()
        try:
            user.save(body['name'],body['email'],body['age'])
        except KeyError:
            missing_fields = [field for field in required_fields if field not in body.keys()]
            raise CustomException(f"{missing_fields} is required!")

        try:
            with open('users_data.json','r',encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(body)

        with open('users_data.json','w',encoding='utf-8') as f:
            json.dump(data,f,indent=4) # noqa

        resp.media = CustomResponse(message="Successfully inserted user").response()

    def custom_exception_handler(self,req,resp,ex,params): # noqa
        if isinstance(ex,CustomException):
            resp.status = ex.status_code
            resp.media = CustomResponse(message=ex.message).response()
        else:
            resp.status = HTTP_500
            resp.media = CustomResponse(message="Internal Server Error!").response()



