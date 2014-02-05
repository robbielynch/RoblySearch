from pymongo import MongoClient
from bson.objectid import ObjectId


class WebsiteMongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def create_website(self, website):
        """
        Inserts a website object into the mongoDB website collection
        """
        website_collection = self.db.websites
        website_id = website_collection.insert({"title": website.title, "url": website.url,
                                                "description": website.description,
                                                "keywords": website.keywords,
                                                "robots_index": website.robots_index,
                                                "h1s": website.h1s,
                                                "links": website.links,
                                                "images": website.images,
                                                "non_html": website.non_html})
        if website_id:
            return True
        else:
            return False

    def read_user(self, email, password):
        users = self.db['users']
        user = users.find_one({"email": email, "password": password})
        return user
