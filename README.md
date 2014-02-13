RoblySearch
===========
A python based search engine, built using the flask micro framework. It stores all of its data in mongodb and
uses Full Text Search to search for website information.

Requirements
-----
- Python 3.*
- Flask
- pymongo
- roblyparser (already included in project)
- stemming.porter2 (already included in project)
- tldextract by John Kurkowski (already included in project)

Backend Features
-----
- Search Query Parser
- Search Query Tokeniser
- Search Query Stemming (Using the porter stemming algorithm)
- Web Crawler
- HTML tokenizer and parser (roblyparser)
- Stemmer (Using the porter stemming algorithm)
- Unit Tests

Frontend Features
--------
- Jinja2 Templates
- Responsive design using [pure css](http://purecss.io/)

MongoDB
-------
Robly uses Full Text Search (FTS) when searching for information from websites.
In order for this to work, you must start your MongoDB server with the normal command
but also append the following to the end of the command:

`--setParameter textSearchEnabled=true`

If your MongoDB resides in MongoHQ's servers, you'll need to email their
support team and ask them to enable Full Text Search for your database.

Installation
---
####Reqiuirements
- Install [Python 3.*](http://www.python.org/getit/)
- Install [pip](http://www.pip-installer.org/en/latest/installing.html)
- Install pymongo: `pip install pymongo`
- Install Flask: `pip install Flask`

####Get RoblySearch
```
git clone https://github.com/robbielynch/RoblySearch.git
```

####Change MongoDB Config
Navigate to RoblySearch/robly_mongo/mongo_config.py

Change the mongo config variables to match that of your mongodb server:
```python
DB_NAME = <<< YOUR_DB_NAME_STRING >>>
HOST = <<< YOUR_HOST_STRING >>> #Default is '127.0.0.1'
PORT = <<< YOUR_PORT_INTEGER >>> #Default is 27017
WEBSITE_COLLECTION = "websites"
USER_COLLECTION = "users"
```

####Run RoblySearch
```
cd RoblySearch
python webapp.py
```

RoblySearch should now be available at http://localhost:9200
