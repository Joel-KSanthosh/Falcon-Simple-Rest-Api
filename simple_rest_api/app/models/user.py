from re import S
from falcon import HTTP_OK
from falcon.status_codes import HTTP_CONFLICT

from bson.json_util import dumps
from bson.json_util import loads

from exception.exception import DatabaseCorruptedException, EmailAlreadyExistException, UserNotFoundException
from settings import collection
from logger import logger

'''Modifying the code to allow pydantic to validate schema'''
from pydantic import BaseModel,PositiveInt,EmailStr


class User(BaseModel):
    name : str
    email : EmailStr
    age : PositiveInt

    @staticmethod
    def __find_user_with_email(email : str):
        return loads(dumps(collection.find({'email' : email},{'_id' : 0})))

    @classmethod
    def find_all_users(cls):
        return loads(dumps(collection.find({},{'_id' : 0})))
    
    def __save(self):
        collection.insert_one({
            'name' : self.email,
            'email' : self.email,
            'age' : self.age
        })

    def create(self):
        result = self.__find_user_with_email(self.email)
        if result:
            if len(result) > 1:
                logger.critical(f"Database Unique Integrity Constraints failed! --- Details Below : \n{result}")
                raise DatabaseCorruptedException()
            raise EmailAlreadyExistException(resp_json='User with given email already exists',status=HTTP_CONFLICT)
        
        self.__save()
        return self.email

    @classmethod
    def find_user_with_email(cls,email : str):
        result = cls.__find_user_with_email(email)
        if result:
            if len(result) > 1:
                raise DatabaseCorruptedException()
            return result
        raise UserNotFoundException(resp_json=f"User with given email {email} doesn't exist!",status=HTTP_OK)
