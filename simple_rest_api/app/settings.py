from calendar import c
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure,ServerSelectionTimeoutError

from logger import logger

load_dotenv()

APP_ENV = os.getenv('DEBUG') == 'True'

if APP_ENV:
    load_dotenv('simple_rest_api/.test.env')
else:
    load_dotenv('simple_rest_api/.dev.env')

MONGO_URI = os.environ.get("MONGO_URI")

MONGO_CLIENT = MongoClient(MONGO_URI)

try:
    server_info = MONGO_CLIENT.server_info()
    logger.info("Connected to MongoDB successfully!")
except OperationFailure as e:
    logger.error("Error connecting to MongoDB : ",e.details.get('errmsg')) # type: ignore
    logger.info(MONGO_URI)
except ServerSelectionTimeoutError as e:
    logger.error("Error connecting to MongoDB : ServerTimeout")
    exit(0)

collection = MONGO_CLIENT.get_default_database().get_collection(name='users')

collection.create_index('email',unique = True)
