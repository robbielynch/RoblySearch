from robly_dto.website import Website
from robly_mongo.website_mongo import WebsiteMongo
import time
import logging
from tldextract import tldextract
from roblyparser.robly_parser import RoblyParser
from google.page_rank import get_page_rank
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

def insert_website_to_mongo(website):
    """
    Function to insert a list of website objects into mongodb
    """
    try:
        mongo = WebsiteMongo()
        mongo.create_website(website)
    except:
        print("[Robly] Error inserting {} into mongodb".format(website.url))

def crawl_website_insert_to_database(url):
    """
    Function to crawl the given url and the pages it links to at a depth of 1.
    Params:     string - the url of the website that is to be crawled
    Returns:    List - of website objects containing each of the crawled websites robly_data
    """
    website = get_website_object(url)
    print("Number of website that will be crawled =", len(website.links))
    if website:
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
                        #website_list.append(website_obj)
                        insert_website_to_mongo(website_obj)
                    time.sleep(1)

def insert_base_url_before_relative_path_links(url, images):
    for n, image in enumerate(images):
        if not image.startswith('http'):
            #Append base url to the image link
            images[n] = merge_link_with_base_url(url, image)
    return images

def is_valid_url(url):
    """
    Checks if the given url is a valid url
    """
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
        print("[Robly] Parsing {}".format(url))
        #Parse website
        parser = RoblyParser()
        html_object = parser.get_webpage_as_object(url)
        pagerank = 0
        try:
            #Get website pagerank from google
            pagerank = get_page_rank(url)
        except:
            pass
        #Create website object
        website = Website(html_object.url, html_object.title, list(set(html_object.h1s)), list(set(html_object.links)),
                          list(set(html_object.images)), html_object.body, html_object.description,
                          list(set(html_object.keywords)), html_object.robots_index, pagerank)
        return website
    except Exception as e:
        print(str(e))
        logging.error("[ROBLY] crawler.py - error parsing website - " + str(e))
        return Website()
