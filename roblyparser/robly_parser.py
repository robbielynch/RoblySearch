import requests
import re
from roblyparser.tokeniser import Tokens
from roblyparser.html_object import HTMLObject
from robly_dto.website import Website

class RoblyParser(object):

    def __init__(self):
        pass

    def get_html(self, url):
        """
        Function to return the HTML content of a url
        """
        headers = {'Accept':'text/css,*/*;q=0.1',
            'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding':'gzip,deflate,sdch',
            'Accept-Language':'en-US,en;q=0.8',
            'User-Agent':'Mozilla/5 (Windows 7) Gecko'}
        res = requests.get(url, headers=headers, timeout=2.0)
        string = str(res.content).replace('\\n', "")
        string = string.replace('&amp;', '&')
        string = string.replace('&#32;', ' ')
        string = string.replace('&#33;', '!')
        string = string.replace('&#34;', '"')
        string = string.replace('&#35;', '#')
        string = string.replace('&#36;', '$')
        string = string.replace('&#37;', '%')
        string = string.replace('&#39;', "'")
        string = string.replace('&#45;', '-')
        string = string.replace('&#032;', ' ')
        string = string.replace('&#033;', '!')
        string = string.replace('&#034;', '"')
        string = string.replace('&#035;', '#')
        string = string.replace('&#036;', '$')
        string = string.replace('&#037;', '%')
        string = string.replace('&#039;', "'")
        string = string.replace('&#045;', '-')

        return string.rstrip()


    def get_webpage_as_object(self, url):
        try:
            html = self.get_html(url)
            if html:
                tokeniser = Tokens()
                tokens = tokeniser.tokenise(html)
                objectifier = HTMLObject()
                objectifier.tokens_to_html_object(tokens, url)
                return objectifier
            else:
                return Website()
        except:
            return Website()