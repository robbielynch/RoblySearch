import re
from stemming.porter2 import stem
from robly_data import stop_words


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
        self.initial_search_query = initial_search_query.lower()

    def extract_context_and_search_query(self):
        """
        Extracts search context and search query from the query.
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
                    self.search_query = prune_string(rest_of_query)

                    #Get context
                    self.search_context = self.initial_search_query[:colon_index]
                    if self.search_context == self.site or self.search_context == self.image or self.search_context == self.document:
                        self.search_context = self.search_context
                        return (self.search_query, self.search_context)
                    else:
                        self.search_context = ""
                        return (self.search_query, self.search_context)
                else:
                    self.search_context = ""
                    self.search_query = prune_string(self.initial_search_query)
                    return (self.search_query, self.search_context)
            else:
                #no context
                #search normally
                self.search_context = ""
                self.search_query = prune_string(self.search_query)
                return (self.search_query, self.search_context)
        else:
            self.search_query = prune_string(self.initial_search_query)
            return (self.search_query, self.search_context)

def prune_string(string):
    """
    Function to remove unwanted character from string,
    remove stop words from string,
    stem the words in the string,
    convert to lowercase
    Params:     string  The string that is to be pruned
    Returns:    string  The pruned string
    """
    string = remove_unwanted_chars(string).lower()
    string = tokenise_string(string)
    string = stem_token_list(string)
    string = remove_stop_words(string)
    string = tokens_to_string(string).lower()
    return string

def remove_unwanted_chars(string):
    """
    Function to remove the unwanted/unnecessary chars from a string
    """
    string = re.sub('[,!.;:#)(\]|"#$%^&_<>~=\[\\{}\(\)]', '', string)
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
    return [value.lower() for value in the_list if value != value_to_be_removed]


def tokens_to_string(tokens):
    return " ".join(tokens)