import re
__author__ = 'robbie'


class HTMLObject(object):
    """
    Class that converts and HTML page into an HTML Object
    """
    url = ""
    title = ""
    description = ""
    h1s = []
    keywords = []
    links = []
    images = []
    body_html = []
    body = ""
    robots_index = True

    def __init__(self):
        pass

    def tokens_to_html_object(self, tokens, url):
        """
        Function to convert a list of html tokens into an HTML object.
        """
        self.url = url
        for index, token in enumerate(tokens):
            #title
            if token.startswith("<title>"):
                self.title = tokens[index + 1]
            elif token.startswith("<body"):
                #Get body html
                body_html_tokens = []
                for t in tokens[index:]:
                    if t.startswith("</body>"):
                        break;
                    if not t.startswith("<body"):
                        body_html_tokens.append(t)
                #Get body content
                self.body_html = body_html_tokens
                self.body = self.get_body_content_as_string_from_body_tokens(body_html_tokens)
            elif token.startswith('<a '):
                #get links
                self.links.append(self.get_link_from_a_href_token(token))
            elif token.startswith('<img '):
                #get links
                self.images.append(self.get_link_from_img_src_token(token))
            elif token.startswith('<h1'):
                #header one
                self.h1s.append(tokens[index+1])
            elif token.startswith('<meta'):
                #Get meta Keywords
                keywords = self.get_keywords_from_meta_tag(token)
                if keywords:
                    if 'keywords' in token:
                        self.keywords = keywords
                else:
                    #Check for meta description
                    if 'description' in token:
                        description = self.get_description_from_meta_tag(token)
                        if description:
                            self.description = description

    def get_link_from_a_href_token(self, token):
        """
        Method to extract the contents of the href variable inside an <a> tag
        e.g
        - token = "<a href='http://google.com'"
        - Will return "http://google.com"
        """
        match = re.search(r'href=[\'"]?([^\'" >]+)', token)
        if match:
            link = match.group(0)
            return link[6:]
        else:
            return ""

    def get_keywords_from_meta_tag(self, token):
        """
        Method to extract keywords from a token.
        Returns a list of keywords
        """
        keywords_string = ""
        keywords_list = []
        #keyword_regex = re.compile(r'<meta\sname=["\']keywords["\']\scontent=["\'](.*?)["\']\s/>')
        match = re.search(r'<meta[\s]*name=[\'"]keywords[\'"][\s]*content=[\'"]([\w, ]*)[\'"][. ]*[/>]*', token)
        try:
            if match:
                content_match = re.search(r'content=[\'"]([\w, ]*)[\'"][. ]*[/>]*', match.group(0))
                keywords_match = re.search(r'content=[\'"]([\w, ]*)[\'"]', content_match.group(0))
                keywords_string = keywords_match.group(0)[9:len(keywords_match.group(0))-1]

            if keywords_string:
                keywords_string = keywords_string.replace(",", " ")
                keywords_list = keywords_string.split()
        except Exception as e:
            print("[RoblyParser] error parsing keywords - {}".format(str(e)))
        return keywords_list

    def get_description_from_meta_tag(self, token):
        """
        Method to extract the meta description from the html token.
        Returns the description or the empty string if not found.
        """
        token = token.replace("\'", r"'")
        token = token.replace("\!", r"!")
        token = token.replace("\-", r"-")
        token = token.replace("\,", r",")
        description_string = ""
        match = re.search('<meta[\s]*name=[\'"]description[\'"][\s]*content=[\'"]([\w, \W]*)[\'"][. ]*[/>]*', token)

        try:
            if match:
                content_match = re.search(r'content=[\'"]([\w, \W\\]*)[\'"][. ]*[/>]*', match.group(0))
                desc_match = re.search(r'content=[\'"]([\w, \W\\]*)[\'"]', content_match.group(0))
                description_string = desc_match.group(0)[9:len(desc_match.group(0))-1]
                return description_string
        except Exception as e:
            print("[RoblyParser] error parsing keywords - {}".format(str(e)))
        return description_string

    def get_body_content_as_string_from_body_tokens(self, body_tokens):
        """
        Returns everything inside <body> </body> tokens as a string
        """
        if body_tokens:
            content_tokens = []
            for t in body_tokens:
                if not t.startswith('<'):
                    content_tokens.append(t)
            if content_tokens:
                body_content = ' '.join(content_tokens)
                return body_content
        return ""

    def get_link_from_img_src_token(self, token):
        """
        Method to extract the image source link inside an <img> tag
        e.g
        - token = "<img src='http://google.com/logo.png'"
        - Will return "http://google.com/logo.png"
        """
        match = re.search(r'src=[\'"]?([^\'" >]+)', token)
        if match:
            link = match.group(0)
            return link[5:]
        else:
            return ""


