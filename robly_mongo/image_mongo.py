from pymongo import MongoClient
from bson.objectid import ObjectId


class ImageMongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def get_images_like(self, query):
        website_collection = self.db.websites
        import re
        regx = re.compile("^" + query, re.IGNORECASE)
        return self.db.website_collection.find({"images": regx})

        #queryRegex = "^" + query
        #cursor = self.db.website_collection.find({"images": {"$regex": queryRegex}})
        #return cursor


