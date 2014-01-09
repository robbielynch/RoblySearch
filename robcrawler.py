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

def getH1s(url):
    soup = BeautifulSoup(getHTML(url))
    h1s = soup.find_all('h1')
    stringh1s = ""
    for h1 in h1s:
        stringh1s += h1.string
        stringh1s += "<br />"
    return stringh1s

def getHTML(url):
    res = requests.get(url)
    return str(BeautifulSoup(res.content))
