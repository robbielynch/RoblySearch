import requests
from bs4 import BeautifulSoup
from website import Website


def get_html(url):
    """
    Function to return the HTML content of a url
    """
    res = requests.get(url)
    return str(BeautifulSoup(res.content))


def get_website_object(url):
    """
    This function parses the url, creates a website object for easy access
    to all html elements that are to be stored in the database.
    Params : url                    The url of the website to be parsed
    Return : website                Website object containing all websites data
    """
    #get html
    html = get_html(url)
    #parse website info
    soup = BeautifulSoup(html)
    #title
    title = get_title(soup)
    #description
    description = get_description(soup)
    #keyword list
    keywords = get_keywords(soup)
    #robots follow
    robots_index = robots_should_index(soup)
    #links
    links = get_links(soup)
    #h1s
    h1s = get_h1s(soup)
    #images
    images = get_images(soup)
    #all page content
    non_html = soup.get_text()

    #Create website object
    website = Website(url, title, h1s, links, images, non_html, description,
                      keywords, robots_index)
    return website


def get_title(soup):
    return soup.title.string


def get_images(soup):
    images = []
    for pic in soup.find_all('img'):
        images.append(pic.get('src'))
    return images


def get_links(soup):
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links


def get_h1s(soup):
    h1s = []
    for h1 in soup.find_all('h1'):
        h1s.append(h1.string)
    return h1s


def get_keywords(soup):
    keyword_string = soup.find("meta", {"name": "keywords"})['content']
    return keyword_string.split(',')


def get_description(soup):
    return soup.find("meta", {"name": "description"})['content']


def robots_should_index(soup):
    if "noindex" in soup.find("meta", {"name": "robots"})['content']:
        return False
    else:
        return True