from pymongo import MongoClient
from bson.objectid import ObjectId
from robly_mongo.mongodb_config import DB_NAME, USER_COLLECTION, HOST, PORT
import logging


class UserMongo:
    def __init__(self):
        self.client = MongoClient(HOST, PORT)
        self.db = self.client[DB_NAME]

    def create_user(self, name, email, password):
        users = self.db[USER_COLLECTION]
        user_id = users.insert({"name": name, "email": email, "password": password})
        if user_id:
            return True
        else:
            return False

    def read_user(self, email, password):
        users = self.db[USER_COLLECTION]
        user = users.find_one({"email": email, "password": password})
        return user
