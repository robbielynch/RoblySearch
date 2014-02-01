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
        qp.extract_context_and_search_query()
        self.assertEqual("site", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_image(self):
        qp = QueryParser("image:my custom search query")
        qp.extract_context_and_search_query()
        self.assertEqual("image", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_doc(self):
        qp = QueryParser("doc:my custom search query")
        qp.extract_context_and_search_query()
        self.assertEqual("doc", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_no_context(self):
        qp = QueryParser("my custom search query")
        qp.extract_context_and_search_query()
        self.assertEqual("", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_search_query_and_context_with_invalid_context(self):
        qp = QueryParser("randomContext:my custom search query")
        qp.extract_context_and_search_query()
        self.assertEqual("", qp.search_context)
        self.assertEqual("my custom search query", qp.search_query)

    def test_remove_unwanted_chars(self):
        qp = QueryParser()
        test_string = "[}a>..,b()>,<c::d~ef~~"
        expected_string = "abcdef"
        self.assertEqual(expected_string, qp.remove_unwanted_chars(test_string))

    def test_remove_unwanted_chars(self):
        qp = QueryParser("test")
        test_string = "this is a test string"
        expected_list = ["this", "is", "a", "test", "string"]
        self.assertEqual(expected_list, qp.tokenise_string(test_string))

    def test_stem_token_list(self):
        tokens = ["actually", "running", "covert", "money", "rabbits"]
        expected_tokens = ["actual", "run", "covert", "money", "rabbit"]
        qp = QueryParser()
        self.assertEqual(expected_tokens, qp.stem_token_list(tokens))

    def tearDown(self):
        pass