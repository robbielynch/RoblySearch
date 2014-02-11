from functools import wraps
import logging
import random
import threading

from flask import Flask, request, session, url_for, redirect, render_template
from robly_mongo.user_mongo import UserMongo
from robly_crawler.crawler import get_website_object
from robly_parser.parser import QueryParser
from robly_mongo.website_mongo import WebsiteMongo
from robly_data.random_search_placeholder import search_placeholders
from robly_crawler import crawler



#Constants
_PORT = 9200
_HOST = '0.0.0.0'
_DEBUG = True

APP_NAME = "robbiesearch"

webapp = Flask(__name__)


def check_loggied_in(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged-in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapped_function


@webapp.route('/')
def root():
    if 'logged-in' in session:
        logged_in = True
    else:
        logged_in = False
    return render_template('index.html', title=APP_NAME, logged_in=logged_in,
                           rand_search=random.choice(search_placeholders))


@webapp.route('/index')
@check_loggied_in
def index():
    if 'logged-in' in session:
        logged_in = True
        return render_template('index.html', title=APP_NAME, logged_in=logged_in, name=session['username'],
                               rand_search=random.choice(search_placeholders))
    else:
        logged_in = False
        return render_template('index.html', title=APP_NAME, logged_in=logged_in,
                               rand_search=random.choice(search_placeholders))



@webapp.route('/signup')
def signup():
    """
    Displays the signup form for potential new users.
    """
    return render_template('index.html', rand_search=random.choice(search_placeholders), logged_in=is_logged_in())


@webapp.route('/login', methods=["GET", "POST"])
def login():
    """
    Displays the login form for potential new users.
    """
    if request.method == "GET":
        if 'logged-in' in session:
            return render_template('/index.html', logged_in=True,
                                   rand_search=random.choice(search_placeholders))
        else:
            return render_template('/index.html', logged_in=False,
                                   rand_search=random.choice(search_placeholders))

    else:
        mongo = UserMongo()
        email = request.form['email']
        password = request.form['password']
        user = mongo.read_user(email, password)
        if user:
            session['logged-in'] = True
            session['username'] = user.__getitem__("name")
            session['useremail'] = user.__getitem__("email")
            return redirect(url_for('index'))
        else:
            return "User not found"


@webapp.route('/logout')
@check_loggied_in
def logout():
    """
    Logs users out. Deletes the current session.
    Returns:
        Redirect - redirects to the login page.
    """
    session.pop('logged-in', None)
    session.pop('useremail', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@webapp.route('/create_new_user', methods=["POST"])
def create_new_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    mongo = UserMongo()
    if mongo.create_user(name, email, password):
        return "User created successfully"
    else:
        return "User not created"

@webapp.route('/search', methods=["POST"])
def search():
    DEBUG_INFO = "[ROBLY] webapp.py - /search - "
    #logging.debug(DEBUG_INFO + "POST request = " + request.form)
    query = request.form['search_box']
    query.strip()
    logging.debug(DEBUG_INFO + "query = " + query)

    #Create query parser object with query string provided by user
    query_parser = QueryParser(query)
    search_query, search_context = query_parser.extract_context_and_search_query()
    if len(query) > 1:
        logging.debug(DEBUG_INFO + "SearchQuery = " + search_query)
        logging.debug(DEBUG_INFO + "SearchContext = " + search_context)
        #query should now have been pruned of unnecessary words and characters
        #Get info from database
        try:
            mongo = WebsiteMongo()
            logging.debug(DEBUG_INFO + "Attempthing to connect with mongodb searchquery='{}' "
                                       "context=''".format(search_query, search_context))
            websites, stats = mongo.search_websites(search_query, search_context)
            #convert microseconds to seconds
            seconds = stats.time_micros / 1000000
            return render_template('search_results.html', search_results=websites, stats=stats, seconds=seconds)
        except Exception as e:
            logging.error(DEBUG_INFO + "Error searching mongodb with the searchquery '{} - {}'".format(search_query,
                                                                                                       str(e)))
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@webapp.route('/index_website', methods=["POST"])
def index_website():
    DEBUG_INFO = "[ROBLY] webapp.py - /index_website - "
    url = request.form['search_box']
    url.strip()
    logging.debug(DEBUG_INFO + "url = " + url)
    #Check if valid url
    if is_valid_url(url) and url.startswith('http'):
        logging.debug(DEBUG_INFO + "'{}' is a valid url")
        #Crawl website in a Thread
        t1 = threading.Thread(target=crawler.crawl_website_insert_to_database, args=(url,))
        t1.start()
        #Return the user to the index page while the thread is executing.
        return render_template('/index.html', logged_in=is_logged_in(),
                                   rand_search=random.choice(search_placeholders),
                                   index_message="'{} is being indexed and will be available to search in a few minutes.'".format(url))
    else:
        logging.error(DEBUG_INFO + "'{}' is not a valid url")
        return render_template('/index.html', logged_in=is_logged_in(),
                                   rand_search=random.choice(search_placeholders),
                                   index_message="Could not index the URL provided - {}".format(url))

@webapp.route('/error_indexing', methods=['GET'])
def error_indexing():
    return render_template('/index.html', logged_in=is_logged_in(),
                                   rand_search=random.choice(search_placeholders),
                                   index_message="Could not index the URL provided")


def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


def is_empty(any_structure):
    """
    Simple helper function to help determine if a robly_data
    structure is empty.
    Parameters:
        Object - Any object
    Returns:
        True - if the object is empty
        False - if the object is not empty
    """
    if any_structure:
        return False
    else:
        return True

def is_logged_in():
    if 'logged-in' in session:
        return True
    else:
        return False


@webapp.route('/crawlall')
def crawlall():
    website = get_website_object("http://roblynch.info")
    output = test_website_contents(website)
    return output


def test_website_contents(website):
    if website:
        string = ""
        if website.url:
            string += "URL = " + website.url
        if website.title:
            string += "<br />Title = " + website.title
        if website.links is not None:
            string += "<br />=============================LINKS===============================================<br />"
            for link in website.links:
                if link is not None:
                    string += link
                    string += "<br />"
            string += "<br />==============================END LINKS==========================================<br />"
        if website.images:
            string += "<br />=============================IMAGES===============================================<br />"
            for img in website.images:
                string += img
                string += "<br />"
            string += "<br />==============================END IMAGES==========================================<br />"
        return string
    else:
        return "No content found in website"


#If it's run directly by the python web system, start it
if __name__ == '__main__':
    #the secret key to encrypt and decrypt cookies
    webapp.secret_key = b'_0\xa5L\x0e\xd3"f\xfe\xbb\x07\xee\xebB?@\xaf.\xa6\xf0\xec\x19\x92\x95\xe6\xb2\xb4\xd1[ \xfad\x8bh\x93\xbf<b\xa5\xccV\xa4$%K4\xa8\xc4'
    webapp.run(host=_HOST, debug=_DEBUG, port=_PORT)
    #We do that because if we use app engine or tornado server
    #it calls it automatically, and uses different ports and namespaces