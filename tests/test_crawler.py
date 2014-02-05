from unittest import TestCase
from robly_crawler.crawler import get_website_object

__author__ = 'robbie'


class TestRobCrawler(TestCase):

    """
    This Class tests the functionality of the QueryParser Class
    """
    website_url = ""
    website = ""

    def setUp(self):
        self.website_url = "http://ierlang.org/t3m60rary111.html"
        self.website = get_website_object(self.website_url)

    def test_title_correct(self):
        self.assertEqual("Test Title", self.website.title)

    def test_h1s_correct(self):
        self.assertEqual(2, len(self.website.h1s))

    def test_url_correct(self):
        self.assertEqual(self.website_url, self.website.url)

    def test_keywords_correct(self):
        self.assertEqual(4, len(self.website.keywords))

    def test_robots_correct(self):
        self.assertTrue(self.website.robots_index)

    def test_images_correct(self):
        self.assertEqual(1, len(self.website.images))

    def test_nonhtml_correct(self):
        self.assertNotEqual("", self.website.non_html)

    def test_links_correct(self):
        self.assertEqual(1, len(self.website.links))

    def test_desc_correct(self):
        self.assertEqual("test description", self.website.description)