RoblySearch
===========

A python based search engine, built using the flask micro framework. It stores all of its data in mongoDB.


- Uses Python 3.3.*
- In its current state - not suited for Google App Engine (GAE uses python 2.7.*)
- Porting to heroku possible (using your own mongoDB host)


Backend Features
================
- Search Query Parser
- Search Query Tokeniser
- Search Query Stemming (Using the porter stemming algorithm)

- Web Crawler
- Web Crawler Parser
- Tokeniser
- Stemmer (Using the porter stemming algorithm)

Frontend Features
=================
- Jinja2 Templates
- JQuery AJAX calls
