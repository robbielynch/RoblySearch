from functools import wraps
import logging

from flask import Flask, request, session, url_for, redirect, render_template
from robly_mongo.user_mongo import UserMongo
from robly_crawler.crawler import get_website_object
from robly_parser.parser import QueryParser
from robly_mongo.website_mongo import WebsiteMongo



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
    return render_template('index.html', title=APP_NAME, logged_in=logged_in)


@webapp.route('/index')
@check_loggied_in
def index():
    if 'logged-in' in session:
        logged_in = True
        return render_template('index.html', title=APP_NAME, logged_in=logged_in, name=session['username'])
    else:
        logged_in = False
        return render_template('index.html', title=APP_NAME, logged_in=logged_in)



@webapp.route('/signup')
def signup():
    """
    Displays the signup form for potential new users.
    """
    return render_template('index.html')


@webapp.route('/login', methods=["GET", "POST"])
def login():
    """
    Displays the login form for potential new users.
    """
    if request.method == "GET":
        if 'logged-in' in session:
            return render_template('/index.html', logged_in=True)
        else:
            return render_template('/index.html', logged_in=False)

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
    logging.warning(DEBUG_INFO + "query = " + query)
    #Create query parser object with query string provided by user
    query_parser = QueryParser(query)
    search_query, search_context = query_parser.extract_context_and_search_query()
    logging.debug(DEBUG_INFO + "SearchQuery = " + search_query)
    logging.debug(DEBUG_INFO + "SearchContext = " + search_context)
    #query should now have been pruned of unnecessary words and characters
    #Get info from database
    mongo = WebsiteMongo()
    websites, stats = mongo.search_websites(search_query, search_context)
    #convert microseconds to seconds
    seconds = stats.time_micros / 1000000
    return render_template('search_results.html', search_results=websites, stats=stats, seconds=seconds)

@webapp.route('/index_website', methods=["POST"])
def index_website():
    logging.warning("in index_website")
    logging.warning(request.form)
    query = request.form['search_box']
    logging.warning("query = " + query)
    #return render_template('search_results.html', search_term=query)
    return query


def is_empty(any_structure):
    """
    Simple helper function to help determine if a data
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