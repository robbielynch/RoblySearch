from pymongo import MongoClient
from bson.objectid import ObjectId
import logging


#An example of a class
class MyMongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def create_user(self, name, email, password):
        users = self.db['users']
        user_id = users.insert({"name": name, "email": email, "password": password})
        if user_id:
            return True
        else:
            return False

    def read_user(self, email, password):
        users = self.db['users']
        user = users.find_one({"email": email, "password": password})
        return user
