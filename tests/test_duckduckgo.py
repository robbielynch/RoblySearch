from unittest import TestCase
from duckduckgo.duckduckgo import query, Redirect, Result, Results, Abstract, Image, Answer
__author__ = 'robbie'


class TestDDG(TestCase):



    def setUp(self):
        pass

    def test_ddg(self):
        result = query('meat')
        string = ""
        related = result.related
        print('')
        for r in related:
            string += '\n----------------\n'
            string += r.url + "\n"
            string += r.text + "\n"
            string += '\n----------------\n'
        self.assertNotEquals("", string)




