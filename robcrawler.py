import requests
from bs4 import BeautifulSoup
from website import Website

def getHTML(url):
    res = requests.get(url)
    return str(BeautifulSoup(res.content))

def getWebsiteInfo(url):
    """
    This function extracts all of the main elements that will be stored in the search engine.
    Params : url                    The url of the website to be parsed
    Return : elementDictionary      Dictionary of main elements of website
    """
    #get html
    html = getHTML(url)
    #parse website info
    soup = BeautifulSoup(html)
    #title
    title = soup.title.string
    #links
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    #h1s
    h1s = []
    for h1 in soup.find_all('h1'):
        h1s.append(h1.string)
    #images
    images = []
    for pic in soup.find_all('img'):
        images.append(pic.get('src'))
    #all page content
    non_html = html

    website = Website(url,title,h1s,links,images,non_html)
    return website


def createElementDictionary(links, h1s, images, non_html):
    elementDictionary = {"links" : links, "h1s" : h1s, "images" : images, "non_html" : non_html}