from pymongo import MongoClient
from bson.objectid import ObjectId


class LinkMongo:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test

    def create_link(self, url):
        link_collection = self.db.links
        is_indexed = self.link_is_indexed(url)
        link_id = link_collection.insert({"url": url, "indexed": is_indexed})
        return link_id

    @staticmethod
    def link_is_indexed(url):
        #TODO - check if the link has already been indexed
        return False

