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

    def search_websites(self, search_query, context=""):
        #self.db.websites.ensureIndex( {type:"text"}, {unique: false, name: "type_index"})
        self.db.websites.create_index(
            [
                ('title', 'text'),
                ('non_html', 'text'),
                ('description', 'text')
            ],
            weights={
                'title': 10,
                'description': 5,
                'non_html': 2
            }
        )
        website_list = self.db.command("text", "websites", search=search_query, limit=10)

        #db.command("text", "players",
        #search="alice",
        #project={"name": 1, "_id": 0},
        #limit=10)

        return website_list
