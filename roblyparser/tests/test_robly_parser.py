__author__ = 'robbie'

from unittest import TestCase
from roblyparser.html_object import HTMLObject
from roblyparser.tokeniser import Tokens
from roblyparser.robly_parser import RoblyParser

class TestRoblyParser(TestCase):

    def setUp(self):
        pass

    def test_get_html(self):
        robly_parser = RoblyParser()
        html = robly_parser.get_html("http://roblynch.info")
        self.assertIsNotNone(html)

    def test_get_webpage_as_object(self):
        robly_parser = RoblyParser()
        html_object = robly_parser.get_webpage_as_object("http://github.com")
        self.assertIsNotNone(html_object)

    def tearDown(self):
        pass