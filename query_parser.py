class QueryParser(object):
    """
    The QueryParser class parses the context and the search query form the string
    typed by the user.
    """
    search_query = ""
    search_context = ""
    initial_search_query = ""


    #Available Context Strings
    site = "site"
    image = "image"
    document = "doc"

    def __init__(self, initial_search_query):
        self.initial_search_query = initial_search_query

    def parse_search_query(self):
        if ":" in self.initial_search_query:
            colon_index = self.initial_search_query.index(':')
            print("colon index = ", colon_index)
            if colon_index >= 0:
                rest_of_query = self.initial_search_query[colon_index + 1:]
                if len(rest_of_query) > 0:
                    #Get the query without the context
                    self.search_query = rest_of_query

                    #Get context
                    self.search_context = self.initial_search_query[:colon_index]
                    if self.search_context == self.site or self.search_context == self.image or self.search_context == self.document:
                        self.search_context = self.search_context
                    else:
                        self.search_context = ""
                else:
                    self.search_context = ""
                    self.search_query = self.initial_search_query
                    #cancel search
            else:
                #no context
                #search normally
                self.search_context = ""
                self.search_query = self.initial_search_query
        else:
            self.search_query = self.initial_search_query
