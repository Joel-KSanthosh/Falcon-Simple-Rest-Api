from falcon.status_codes import HTTP_CONFLICT

from simple_rest_api.app.exception.exception import CustomException
from simple_rest_api.app.settings import collection
from pymongo.errors import DuplicateKeyError
from email_validator import validate_email,EmailNotValidError

class User:

    @staticmethod
    def validate_email(email):
        try:
            validate_email(email)
            return email
        except EmailNotValidError:
            raise CustomException("Enter a valid email!")

    def validate_data(self,name,email,age):
        try:
            age = int(age)
        except ValueError:
            raise CustomException("Enter a valid age for age!")

        validated_data = {
            "name": name,
            "email": self.validate_email(email),
            "age": age

        }
        return validated_data

    def save(self,name,email,age):
        validated_data = self.validate_data(name, email, age)
        try:
            collection.insert_one(validated_data)
        except DuplicateKeyError:
            raise CustomException("Email already exist!",HTTP_CONFLICT)

    @classmethod
    def find_user_with_email(cls, email):
        return collection.find_one({'email' : email},{'_id': 0})

    @classmethod
    def find_all_user(cls):
        return collection.find({},{'_id':0})
