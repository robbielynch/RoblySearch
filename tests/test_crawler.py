from unittest import TestCase
from robly_crawler.crawler import get_website_object, crawl_website_insert_to_database, merge_link_with_base_url
import threading

__author__ = 'robbie'


class TestRobCrawler(TestCase):

    """
    This Class tests the functionality of the QueryParser Class
    """
    website_url = ""
    website = ""

    def setUp(self):
        self.website_url = "http://roblynch.info/about"
        self.website = get_website_object(self.website_url)
        print("done")

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
        print(self.website.non_html)
        self.assertNotEqual("", self.website.non_html)

    def test_links_correct(self):
        self.assertEqual(1, len(self.website.links))

    def test_desc_correct(self):
        self.assertEqual("test description", self.website.description)

    def test_crawl_website_insert_to_database(self):
        urls = ["http://play.google.com", "https://news.google.ie/"]
        for url in urls:
            crawl_website_insert_to_database(url)
            print("Crawl complete on -", url)
        print("done")

    def test_merge_link_with_base_url(self):
        url = "http://roblynch.info/blog/awesomeness"
        link = "/static/imgs/logo.png"
        expected = "http://roblynch.info/static/imgs/logo.png"
        merged_string = merge_link_with_base_url(url, link)
        self.assertEqual(expected, merged_string)


    def test_crawl_these_major_sites(self):
        urls =  [
                    "http://play.google.com", "https://news.google.ie/",
                    "http://facebook.com", "http://amazon.com",
                    "http://bookdepository.com", "http://mongohq.com",
                    "http://roblynch.info", "http://ierlang.org", "http://erlang.org",
                    "http://python.org", "http://github.com", "http://bitbucket.org",
                    "http://hackerrank.com", "http://stackoverflow.com", "http://yahoo.com",
                    "http://google.com", "http://bing.com", "http://microsoft.com",
                    "http://aol.ie", "http://wikipedia.com"
                ]
        for url in urls:
            t1 = threading.Thread(target=crawl_website_insert_to_database, args=(url,))
            t1.start()
            print("Crawling -", url)
        print("done")