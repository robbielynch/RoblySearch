import requests
from bs4 import BeautifulSoup
from robly_dto.website import Website
from robly_parser import parser
import time


def get_html(url):
    """
    Function to return the HTML content of a url
    """
    headers = {'Accept':'text/css,*/*;q=0.1',
        'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language':'en-US,en;q=0.8',
        'User-Agent':'Mozilla/5 (Windows 7) Gecko'}
    res = requests.get(url, headers=headers)
    return str(BeautifulSoup(res.content))

def crawl_website_insert_to_database(url):
    """
    Function to crawl the given url and the pages it links to.

    """
    website = get_website_object(url)
    if website:
        website_list = [website]
        if website.links:
            for w in website.links:
                if w != url and not '#' in w and w.startswith('http'):
                    website_obj = get_website_object(w)
                    website_list.append(website_obj)
                time.sleep(2)
        return website_list
    return []






def get_website_object(url):
    """
    This function parses the url, creates a website object for easy access
    to all html elements that are to be stored in the database.
    Params : url                    The url of the website to be parsed
    Return : website                Website object containing all websites data
    """
    print("crawling - ", url)
    #get html
    try:
        html = get_html(url)
    except Exception:
        pass
    #parse website info
    try:
        soup = BeautifulSoup(html)
    except Exception:
        pass

    if soup:
        #title
        try:
            title = get_title(soup)
        except Exception:
            title = ""
        #description
        try:
            description = get_description(soup)
        except Exception:
            description = ""
        #keyword list
        try:
            keywords = get_keywords(soup)
        except Exception:
            keywords = []
        #robots follow
        try:
            robots_index = robots_should_index(soup)
        except Exception:
            robots_index = True
        #links
        try:
            links = get_links(soup)
        except Exception:
            links = []
        #h1s
        try:
            h1s = get_h1s(soup)
        except Exception:
            h1s = []
        #images
        try:
            images = get_images(soup)
        except Exception:
            images = []
        ## Get the text of the web page
        try:
            non_html = soup.get_text()
            non_html = parser.prune_string(non_html)
        except Exception:
            non_html = ""

        #Create website object
        website = Website(url, title, h1s, links, images, non_html, description,
                          keywords, robots_index)
        return website
    else:
        return None


def get_title(soup):
    """
    Returns the title of the web page
    """
    return soup.title.string


def get_images(soup):
    """
    Returns: A list of URL for images found on the page
    """
    images = []
    for pic in soup.find_all('img'):
        images.append(pic.get('src'))
    return images


def get_links(soup):
    """
    Returns:    A list of url links found on the page.
    """
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links


def get_h1s(soup):
    """
    Returns:    A list of header 1 tags found on the web page
    """
    h1s = []
    for h1 in soup.find_all('h1'):
        h1s.append(h1.string)
    return h1s


def get_keywords(soup):
    """
    Returns:    A list of keywords found in the meta tags of the webpage
    """
    keyword_string = soup.find("meta", {"name": "keywords"})['content']
    return keyword_string.split(',')


def get_description(soup):
    """
    Returns:    A string description of the website found in the meta tags in the website
    """
    return soup.find("meta", {"name": "description"})['content']


def robots_should_index(soup):
    """
    Returns:    True if the web page wants to be indexed
                False if the web page does not want to be indexed
    """
    if "noindex" in soup.find("meta", {"name": "robots"})['content']:
        return False
    else:
        return True