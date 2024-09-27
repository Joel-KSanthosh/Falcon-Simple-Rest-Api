import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure,ServerSelectionTimeoutError

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB")

MONGO_CLIENT = MongoClient(host=MONGO_URI, serverSelectionTimeoutMS=3000)

try:
    server_info = MONGO_CLIENT.server_info()
    print("Connected to MongoDB successfully!")
except OperationFailure as e:
    print("Error connecting to MongoDB : ",e.details.get('errmsg'))
except ServerSelectionTimeoutError as e:
    print("Error connecting to MongoDB : ServerTimeout")
    exit(0)

db = MONGO_CLIENT[MONGO_DB]

collection = db.users

collection.create_index('email',unique = True)
