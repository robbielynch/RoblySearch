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
    	user_id = users.insert({"name" : name, "email" : email, "password" : password})
    	return str(user_id)