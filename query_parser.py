import re
from stemming.porter2 import stem


class QueryParser(object):
    """
    The QueryParser class parses the context and the search query form the string
    typed by the user.
    """
    search_query = ""
    search_context = ""
    initial_search_query = ""
    search_tokens = []
    stemmed_tokens = []

    #Available Context Strings
    site = "site"
    image = "image"
    document = "doc"

    def __init__(self, initial_search_query=""):
        self.initial_search_query = initial_search_query

    def extract_context_and_search_query(self):
        """
        Searches for, and extracts, context in search query.
        Search query then broken down into:
        - Context
        - Search Query
        """
        if ":" in self.initial_search_query:
            colon_index = self.initial_search_query.index(':')
            print("colon index = ", colon_index)
            if colon_index >= 0:
                rest_of_query = self.initial_search_query[colon_index + 1:]
                if len(rest_of_query) > 0:
                    #Get the query without the context
                    self.search_query = self.remove_unwanted_chars(rest_of_query)

                    #Get context
                    self.search_context = self.initial_search_query[:colon_index]
                    if self.search_context == self.site or self.search_context == self.image or self.search_context == self.document:
                        self.search_context = self.search_context
                    else:
                        self.search_context = ""
                else:
                    self.search_context = ""
                    self.search_query = self.remove_unwanted_chars(self.initial_search_query)
            else:
                #no context
                #search normally
                self.search_context = ""
                self.search_query = self.remove_unwanted_chars(self.initial_search_query)
        else:
            self.search_query = self.remove_unwanted_chars(self.initial_search_query)

    @staticmethod
    def remove_unwanted_chars(string):
        """
        Function to remove the unwanted/unnecessary chars from a string
        """
        string = re.sub('[,!.;:#)(\]<>~=\[\\{}\(\)]', '', string)
        return string

    @staticmethod
    def tokenise_string(string):
        return string.split()

    def stem_token_list(self, words):
        stemmed_tokens = []
        for word in words:
            w = stem(word)
            stemmed_tokens.append(w)
        return stemmed_tokens
