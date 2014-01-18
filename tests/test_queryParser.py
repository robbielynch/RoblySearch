from unittest import TestCase
from query_parser import QueryParser

__author__ = 'robbie'


class TestQueryParser(TestCase):

    """
    This Class tests the functionality of the QueryParser Class
    """

    def setUp(self):
        pass

    def test_search_query_and_context_with_site(self):
        qp = QueryParser("site:my custom search query")
        qp.parse_search_query()
        self.assertEqual("site", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_image(self):
        qp = QueryParser("image:my custom search query")
        qp.parse_search_query()
        self.assertEqual("image", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_doc(self):
        qp = QueryParser("doc:my custom search query")
        qp.parse_search_query()
        self.assertEqual("doc", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_no_context(self):
        qp = QueryParser("my custom search query")
        qp.parse_search_query()
        self.assertEqual("", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_invalid_context(self):
        qp = QueryParser("randomContext:my custom search query")
        qp.parse_search_query()
        self.assertEqual("", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)