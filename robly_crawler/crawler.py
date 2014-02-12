import requests
from bs4 import BeautifulSoup
from robly_dto.website import Website
from robly_mongo.website_mongo import WebsiteMongo
import time
import logging
from tldextract import tldextract
from roblyparser.robly_parser import RoblyParser
from roblyparser.html_object import HTMLObject



def get_base_url(url):
    """
    Takes as input a url, returns the protocol,domain and suffix concatenated
    to form the base url of the website. Uses the tldextract library.
    """
    tld = tldextract.extract(url)
    print(tld.subdomain, ' - ', tld.domain, ' - ', tld.suffix)
    if tld.subdomain != "":
        base_url = '.'.join([tld.subdomain, tld.domain, tld.suffix])
    else:
        base_url = '.'.join([tld.domain, tld.suffix])
    return base_url

def get_protocol(url):
    """
    Returns whether the url is https or http and returns the protocol as a string
    """
    if url.startswith('https'):
        protocol = "https://"
    else:
        protocol = "http://"
    return protocol

def get_protocol_without_slashes(url):
    """
    Returns whether the url is https or http and returns the protocol as a string
    """
    if url.startswith('https'):
        protocol = "https:"
    else:
        protocol = "http:"
    return protocol


def merge_link_with_base_url(url, link):
    """
    Function that gets the base url of the passed url, and merges it with the
    passed link and returns the concatenated string.
    e.g. When url = 'http://roblynch.info/awesome/stuff'
    and link = '/static/images/logo.png'
    The resulting merged string will look like "http://roblynch.info/static/image/logo.png"
    Params:     url - a string containing the url to be merged with the link
                link - the string link to be appended to the base_url.
                       Only links beginning with '/' are accepted
    Returns:    A merged string containing:
                The protocol of the url, the merged base url and the link
    """
    #Get protocol
    protocol = get_protocol(url)
    #Get base url
    base_url = get_base_url(url)
    #Join protocol to base url to link
    if link.startswith('/'):
        merged_string = protocol + base_url + link
    else:
            merged_string = protocol + base_url + '/' + link
    return merged_string


def insert_websites_to_mongo(website_list):
    """
    Function to insert a list of website objects into mongodb
    """
    mongo = WebsiteMongo()
    for w in website_list:
        print("Inserting", w.url, "into mongodb")
        mongo.create_website(w)


def crawl_website_insert_to_database(url):
    """
    Function to crawl the given url and the pages it links to at a depth of 1.
    Params:     string - the url of the website that is to be crawled
    Returns:    List - of website objects containing each of the crawled websites robly_data
    """
    website = get_website_object(url)
    print("Number of website that will be crawled =", len(website.links))
    if website:
        website_list = [website]
        if website.links:
            for w in website.links:
                if w:
                    if w.startswith('//'):
                        w = get_protocol_without_slashes(w) + w
                    #Append base url to beginning of links beginning with /
                    if w.startswith('/'):
                        w = merge_link_with_base_url(website.url, w)
                    #Crawl the valid links
                    if w != url and is_valid_url(w):
                        website_obj = get_website_object(w)
                        website_list.append(website_obj)
                    time.sleep(2)
        insert_websites_to_mongo(website_list)

def insert_base_url_before_relative_path_links(url, images):
    for n, image in enumerate(images):
        if not image.startswith('http'):
            #Append base url to the image link
            images[n] = merge_link_with_base_url(url, image)
    return images

def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)

def get_website_object(url):
    """
    This function uses the custom built parser (roblyparser) to parse the url,
    creates a website object for easy access
    to all html elements that are to be stored in the database.
    Params : url        The url of the website to be parsed
    Return : website    Website object containing all websites robly_data
    """
    try:
        parser = RoblyParser()
        html_object = parser.get_webpage_as_object(url)

        website = Website(html_object.url, html_object.title, html_object.h1s, html_object.links,
                          html_object.images, html_object.body, html_object.description,
                          html_object.keywords, html_object.robots_index)
        return website
    except Exception as e:
        print(str(e))
        logging.error("[ROBLY] crawler.py - error parsing website - " + str(e))
        return Website()


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