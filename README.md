RoblySearch
===========

A python based search engine, built using the flask micro framework. It stores all of its data in mongodb and
uses Full Text Search to search for website information.

Requirements
============
- Python 3.*
- BeautifulSoup
- Flask
- pymongo
- stemming.porter2 (already included in project)
- tldextract by John Kurkowski (already included in project)

Backend Features
================
- Search Query Parser (using BeautifulSoup)
- Search Query Tokeniser
- Search Query Stemming (Using the porter stemming algorithm)
- Web Crawler
- Web Crawler Parser
- Tokeniser
- Stemmer (Using the porter stemming algorithm)
- Mongo Classes
- Unit Tests

Frontend Features
=================
- Jinja2 Templates
- JQuery AJAX calls

MongoDB
=======
Robly uses Full Text Search (FTS) when searching for information from websites.
In order for this to work, you must start your MongoDB server with the normal command
but also append the following to the end of the command:

`--setParameter textSearchEnabled=true`

