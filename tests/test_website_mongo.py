from unittest import TestCase
from robly_mongo.website_mongo import WebsiteMongo
from robly_dto.website import Website

__author__ = 'robbie'


def generate_website():
    website = Website()
    website.url = "http://thisisanexampleroblyurl.com"
    website.description = "Sample description of robly website"
    website.h1s = ["Awesome", "Amazing"]
    website.images = ["http://static3.wikia.nocookie.net/__cb20130606164014/animalcrossing/images/3/30/Monkey.jpg",
                      "http://www.thelostogle.com/wp-content/uploads/2013/12/happy-monkey-550x366.jpg"]
    website.keywords = ["one keyword", "two keyword", "three keyword"]
    website.links = ["http://google.com", "http://facebook.com", "http://play.google.com"]
    website.robots_index = True
    website.title = "Super Awesome Battery Stuff"
    website.non_html = """
    A new nanotechnology that doubles the life of smartphone, laptop and electric-vehicle batteries even after being charged and discharged more than 1,000 times has been developed by researchers at the University of Limerick.
    The breakthrough means the research team could be tapping into a market estimated to be worth US$53.7bn by 2020.
    “We have developed a new germanium nanowire-based anode that has the ability to greatly increase the capacity and lifetimes of lithium-ion batteries,” said lead researcher Dr Kevin Ryan.
    The research published by the journal Nano Letters outlines the findings.
    “This breakthrough is important for mobile computing and telecoms but also for the emerging electric-vehicle market, allowing for smaller and lighter batteries that can hold more charge for longer and maintain this performance over the lifetime of the product.”
    Small is the next big thing
    The research team has also ensured its nanotechnology solution is scalable, low-cost and low-energy, making the technology both greener and commercially viable.
    The research has been supported by Science Foundation Ireland (SFI) under the Principal Investigator Program to Dr Kevin Ryan and also by EU funding through the GREENLION Project.
    “The typical lithium-ion battery on the market today is based on graphite and has a relatively low capacity. This limits the amount of energy which can be stored. In our research we used an alternative element, germanium, which is of a higher capacity,” Ryan said.
    “The challenge has been that the material expands quite dramatically during charging and falls apart after a relatively small number of cycles.
    “By using nanotechnology, we have found a way to restructure germanium, in the form of nanowires, into a stable porous material that is an ideal battery material as it remains stable over very long time scales during continued operation,” Ryan added.
    """
    return website


class TestWebsiteMongo(TestCase):

    """
    This Class tests the functionality of the website_mongo class
    """

    def setUp(self):
        pass

    def test_create_insert_website(self):
        mongo = WebsiteMongo()
        website = generate_website()
        successful = mongo.create_website(website)
        print("blah")

    def test_search_website(self):
        #Uses Full Text Search
        #MongoDB server must be started with command "--setParameter textSearchEnabled=true"
        #in order for FTS to be enabled
        mongo = WebsiteMongo()
        query = "git"
        websites_list, stats_obj = mongo.search_websites(query)
        self.assertIsNotNone(websites_list)
        self.assertIsNotNone(stats_obj)

    #def test_delete_websites(self):
    #    mongo = WebsiteMongo()
    #    mongo.delete_websites()

    def tearDown(self):
        pass