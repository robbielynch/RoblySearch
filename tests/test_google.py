from unittest import TestCase
from google.page_rank import get_page_rank

__author__ = 'robbie'


class TestGooglePageRank(TestCase):

    """
    This Class tests the functionality of the QueryParser Class
    """
    website_url = ""
    website = ""

    def setUp(self):
        pass

    def test_getpr(self):
        pr = get_page_rank("http://stackoverflow.com/questions/15014310/python3-xrange-lack-hurts")
        self.assertIsNotNone(pr)

