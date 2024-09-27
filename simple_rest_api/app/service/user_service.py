import json

from falcon import HTTP_400
from pydantic import ValidationError

from exception.exception import ValidationException
from models.user import User
from logger import logger


class UserService:
    @staticmethod
    def find(email):
        if email:
            return User.find_user_with_email(email)
        else:
            return User.find_all_users()

    @staticmethod
    def create(body):
        try:
            user = User(**body)
            email = user.create()
        except ValidationError as exc:
            error_list = []
            for errors in exc.errors():
                error_list.append('{} : {}'.format(errors.get('loc')[0],errors.get('msg')))
                
            raise ValidationException(resp_json=error_list,status=HTTP_400) # type: ignore

        try:
            with open('users_data.json','r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(body)

        with open('users_data.json','w') as f:
            data_str = json.dumps(data,indent=4)
            f.write(data_str)

        return email
