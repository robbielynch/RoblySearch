from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import inspect
from robly_dto.stats import Statistics
from robly_dto.website import Website
from robly_mongo.mongodb_config import DB_NAME, WEBSITE_COLLECTION, HOST, PORT


class WebsiteMongo:
    DEBUG_INFO = "[Robly] WebsiteMongo - "

    def __init__(self):
        self.client = MongoClient(HOST, PORT)
        self.db = self.client[DB_NAME]
        logging.warning(self.DEBUG_INFO + "HOST={}\nPORT={}\nDB_NAME={}".format(HOST,PORT,DB_NAME))

    def create_website(self, website):
        """
        Inserts a website object into the mongoDB website collection
        """
        website_collection = self.db[WEBSITE_COLLECTION]

        website_id = website_collection.update({
                                                    #Query
                                                    "url": website.url
                                               },
                                                {
                                                    #Field Data to insert/update
                                                    "title": website.title, "url": website.url,
                                                    "description": website.description,
                                                    "keywords": website.keywords,
                                                    "robots_index": website.robots_index,
                                                    "h1s": website.h1s,
                                                    "links": website.links,
                                                    "images": website.images,
                                                    "non_html": website.non_html,
                                                    "pagerank": website.pagerank
                                                },
                                                ##Set Upsert to True##
                                                #Insert if it doesn't exist
                                                #Update if it already exists
                                                True)
        if website_id:
            return True
        else:
            return False

    def search_websites(self, search_query, context=""):
        """
        Function to do a full text search on all indexed websites.
        @param  search_query    - the query to use in the full text search
        @param  context         - what to search for (sites, images, documents)
        @return tuple           - containing (list_of_website_objects, statistics_object)
        """
        #TODO - return proper results that match context
        #self.db.websites.ensureIndex( {type:"text"}, {unique: false, name: "type_index"})
        #Uses Full Text Search
        #MongoDB server must be started with command "--setParameter textSearchEnabled=true"
        #in order for FTS to be enabled
        try:
            self.db.websites.create_index(
                [
                    ('title', 'text'),
                    ('url', 'text'),
                    ('description', 'text')
                ],
                weights={
                    'title': 6,
                    'description': 5,
                    'url': 2,
                }
            )

            #Search
            results_dict = self.db.command("text",
                                           "websites",
                                            search=search_query,
                                            #projection={
                                            #    'non_html': False
                                            #},
                                            limit=100)

            #db.command("text", "players",
            #search="alice",
            #project={"name": 1, "_id": 0},
            #limit=10)

            return self.convert_mongo_result_to_list_of_websites(results_dict)
        except Exception as e:
            logging.error(self.DEBUG_INFO + inspect.stack()[0][3] + " - ERROR searching database - " + str(e))

    def convert_mongo_result_to_list_of_websites(self, results_dict):
        """
        Function to convert mongo's result dictionary to a list of website objects
        and a statistics object.
        """
        search_query_stats_dict = results_dict['stats']
        results_list = results_dict['results']
        website_list = []
        for w in results_list:
            score = w['score']
            website = self.convert_dict_to_website_object(w['obj'])
            website.score = score
            website_list.append(website)
        return website_list, self.covert_dict_to_statistics_object(search_query_stats_dict)

    def convert_dict_to_website_object(self, website_dict):
        """
        Dictionary to Website object.
        """
        website = Website()
        website.url = website_dict['url']
        website.description = website_dict['description']
        website.h1s = website_dict['h1s']
        website.images = website_dict['images']
        website.keywords = website_dict['keywords']
        website.links = website_dict['links']
        website.robots_index = website_dict['robots_index']
        website.title = website_dict['title']
        website.non_html = website_dict['non_html']
        try:
            website.pagerank = website_dict['pagerank']
        except:
            pass
        return website

    def covert_dict_to_statistics_object(self, stats_dict):
        """
        Dictionary to Statistics object
        """
        stats = Statistics(stats_dict['n'], stats_dict['nfound'],
                           stats_dict['nscanned'],
                           stats_dict['nscannedObjects'],
                           stats_dict['timeMicros'])
        return stats
