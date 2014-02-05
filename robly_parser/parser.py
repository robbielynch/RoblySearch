import re
from stemming.porter2 import stem
from data import stop_words


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
                    self.search_query = remove_unwanted_chars(rest_of_query)

                    #Get context
                    self.search_context = self.initial_search_query[:colon_index]
                    if self.search_context == self.site or self.search_context == self.image or self.search_context == self.document:
                        self.search_context = self.search_context
                    else:
                        self.search_context = ""
                else:
                    self.search_context = ""
                    self.search_query = remove_unwanted_chars(self.initial_search_query)
            else:
                #no context
                #search normally
                self.search_context = ""
                self.search_query = remove_unwanted_chars(self.initial_search_query)
        else:
            self.search_query = remove_unwanted_chars(self.initial_search_query)


def remove_unwanted_chars(string):
    """
    Function to remove the unwanted/unnecessary chars from a string
    """
    string = re.sub('[,!.;:#)(\]<>~=\[\\{}\(\)]', '', string)
    return string

def tokenise_string(string):
    """
    Splits the passed string into a list of strings, delimited by a space character
    """
    return string.split()

def stem_token_list(words):
    """
    Function that uses the porter stemming algorithm to remove suffixes(and in some cases prefixes)
    in order to find the "root word" or stem of a given word.
    """
    stemmed_tokens = []
    for word in words:
        w = stem(word)
        stemmed_tokens.append(w)
    return stemmed_tokens

def remove_stop_words(tokens):
    """
    Removes the list of imported stop_words from the list of tokens
    """
    for word in stop_words.STOP_WORDS:
        tokens = remove_values_from_list(tokens, word)
    return tokens

def remove_values_from_list(the_list, value_to_be_removed):
    """
    This function removes a given value from the given list
    Returns:    The list, minus all occurrences of value_value_to_be_removed
    """
    return [value for value in the_list if value != value_to_be_removed]


def tokens_to_string(tokens):
    return " ".join(tokens)