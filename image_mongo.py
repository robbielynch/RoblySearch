from pymongo import MongoClient
from bson.objectid import ObjectId


class ImageMongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def create_image(self, url):
        image_collection = self.db.images
        if self.image_exists_already(url):
            return 0
        else:
            return image_collection.insert({"url": url})

    @staticmethod
    def image_exists_already(url):
        #TODO - check if the link has already been indexed
        return False

