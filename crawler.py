# -*- coding: utf-8 -*-
import re
import os
#import md5
import random
from pymongo import Connection
from urllib.request import urlopen


# def db_connect():
#         connection = Connection('localhost', 27017)
#         db = connection.search
#         #db.authenticate('search', '123123')
#         return db

# pages = db_connect().pages
# to_work = db_connect().to_work

def get_links(url):
        page = urlopen(url).read()
        # Get all links from index page
        r = r'<a.*href=[\'"]?([^\'" >]*)'
        links = re.findall(r, page)
        output = []
        for link in links:
                # if href="/..."
                if link[0] == '/' and site + link not in output and not pages.find_one({'url': site + link}):
                        output.append(site + link)
                # if href have "http://site_url.com"
                if re.search(site, link) and link not in output and not pages.find_one({'url': link}):
                        output.append(link)
        print(output)
        return output
        # return page
        
# def add_page(url):
#         content = urlopen(site).read()
#         if not pages.find_one({'url': url}):
#                 hash = md5.new()
#                 hash.update(url)

#                 page_id = pages.save({
#                     'url': url,
#                     'content': content, 
#                     'md5': hash.hexdigest()
#                 })
#                 to_work.save({ 'url': url })

# def parse(url):
#         links = get_links(url)
#         print(links)
#         for link in links:
#                 print("Find link" + link)
#                 if not pages.find_one({'url': link}):
#                         add_page(link)
#                         print("В базу добавлена страница " + link)
#         to_work.remove({'url': url})

# def main():
#         print("Страниц в базе: " + str(pages.find().count()))
#         if not pages.find_one({'url': site}):
#                 index_links = get_links(site)
#                 for link in index_links:
#                         if not pages.find_one({'url': link}):
#                                 add_page(link)
#                                 print("В базу добавлена страница " + link)

#         for url in to_work.find():
#                 print("Parsing " + url['url'])
#                 parse(url['url'])
        



if __name__ == '__main__':
        db_connect()
        main()