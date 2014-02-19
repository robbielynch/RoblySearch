__author__ = 'Robbie'

"""
MonggoDB Configuration Variables.

DB_NAME
    The name of the database in your mongodb server.
HOST
    The address where your mongodb server resides.
    Automatically set to 127.0.0.1 (localhost).
PORT
    The port that your mongodb server uses.
    Default = 27017
    List of default ports can be found at:
    http://docs.mongodb.org/manual/reference/default-mongodb-port/
WEBSITE_COLLECTION
    The name of the collection where documents containing
    website information is stored.
    Automatically created if it does not exist.
USER_COLLECTION
    The name of the collection where documents containing
    user information is stored.
    Automatically created if it does not exist.
"""

#DB_NAME = "roblysearch"
#HOST = '127.0.0.1'
#PORT = 27017
#WEBSITE_COLLECTION = "websites"
#USER_COLLECTION = "users"



#MongoHQ
DB_NAME = "robbiesearch"
PORT = 10080
HOST = 'mongodb://robly:robly@alex.mongohq.com:' + str(PORT) + '/' + DB_NAME
WEBSITE_COLLECTION = "websites"
USER_COLLECTION = "users"