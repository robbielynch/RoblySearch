import requests
from bs4 import BeautifulSoup

def getLinks(url):
    soup = BeautifulSoup(getHTML(url))
    links = soup.find_all('a')
    stringlinks = ""
    for link in links:
        stringlinks += link.get('href')
        stringlinks += "<br />"
    return stringlinks

def getHTML(url):
    res = requests.get(url)
    return str(BeautifulSoup(res.content))
