__author__ = 'robbie'


class Tokens(object):

    tokens = []
    html = ""

    def __init__(self):
        pass

    def tokenise(self, html):
        """
        Function to tokenise all HTML tags and to tokenise the string content
        between each tag.
        @param  html    The html to be tokenised
        @return list    List of tokens
        """
        html = html.lower()
        #tokens are <stuff inside here> and  > stuff outside here </
        for index, c in enumerate(html):

            if c == '<':
                # If we reach the beginning of a tag
                # extract the tag and insert into the token list
                tag, index = self.get_tag(html, index)
                self.tokens.append(tag)
            elif c == '>':
                # If we reach the end of a tag
                # extract the content between the end of the tag
                # and the next starting tag.
                # Then insert into the token list
                string_content, index = self.get_string_content(html, index)
                if string_content:
                    self.tokens.append(string_content)

        return self.tokens

    def get_tag(self, html, index):
        """
        Given the html string and the index of the opening tag <
        This function extracts the full tag and returns it
        e.g.
        HTML = <a href="#">my_link</a>
        INDEX = 0
        The returned string will be = "<a href='#'>"
        """
        endTagIndex = 0
        html = html[index:]
        for ind, c in enumerate(html):
            if c == ">":
                endTagIndex = ind
                break
        tag = html[:endTagIndex+1]
        return tag, endTagIndex+1

    def get_string_content(self, html, index):
        """
        Given the html string and the index of the last closing tag >
        This function extracts the content of everything between the
        closing tag and the next opening tag <
        e.g.
        HTML = "<a href='#'>my_link</a>"
        INDEX = 11
        The returned string will be = "my_link"
        """
        end_index = 0
        html = html[index:]
        for ind, c in enumerate(html):
            if c == "<":
                end_index = ind
                break
        string_content = html[1:end_index]
        return string_content.strip(), end_index