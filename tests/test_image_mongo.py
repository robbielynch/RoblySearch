from unittest import TestCase
from robly_mongo.image_mongo import ImageMongo

__author__ = 'robbie'


class TestImageMongo(TestCase):

    """
    This Class tests the functionality of the QueryParser Class
    """

    def setUp(self):
        pass

    def test_search_query_and_context_with_site(self):
        im = ImageMongo()
        results = im.get_images_like("http")
        print("printing results")
        for i in results:
            print("printing i")
            print(i)
        #self.assertEqual("site", im.search_context)
        #self.assertEqual("my custom search query", im.search_query)


    def tearDown(self):
        pass