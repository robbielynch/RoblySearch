"""
Name 			: Robbie Lynch

Student Number 	: C00151101

Program			: Web Application to produce a login system where it is possible to create users, activate users,
				  assign permissions, limit access to pages based on permissions, create a session for the user.
				  Built using the flask framework.

Things to note 	: 1. The pilots code is on line number 117
				  2. Every block of useful and reusable code has been extracted to its own function (hence the large number of funs)
				  3. The users are stored in a json file located at /users/users.json
				  4. The users waiting to be activated are stored in a json file located at /waiting/waiting.json
				  5. The flights information is stored in a json file located at /flights/flights.json
				  6. Function Decorators are at the top of the file
				  7. Web App route directories are next
				  8. Then the helper functions follow that.
				  9. I've included a couple of CSS files located in /static/css/*. I did not write these.
				  10. When the index/home page template loads, only the admin can see the extra section with admin options.
				  11. Ficticious: This web app is now suitable for cats
"""
from flask import Flask, request, send_file, abort, make_response, session, escape, url_for, redirect, render_template
from functools import wraps
import logging
from mymongo import MyMongo
from bson.objectid import ObjectId


#Constants
_PORT = 9200
_HOST = '0.0.0.0' #this will find the current ip address and use it
_DEBUG = True

webapp = Flask(__name__)  #main namespace


def check_loggied_in(func):
	@wraps(func) 
	def wrapped_function(*args, **kwargs):
		if 'logged-in' in session:
			return func(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrapped_function


@webapp.route('/')
@check_loggied_in
def index():
	email = session['email']
	return render_template('home.html', title='Home', stylesheet='home-stylesheet.css', 
							username=username, usertype=usertype)

@webapp.route('/signup')
def signup():
	"""
	Displays the signup form for potential new users.
	"""
	return render_template( 'signup.html', title = "Sign Up", stylesheet = "login-stylesheet.css")

@webapp.route('/login', methods=["GET","POST"])
def login():
	"""
	Displays the login form for potential new users.
	"""
	if request.method == "GET":
		return render_template( 'login.html' , title = "Login", stylesheet = "login-stylesheet.css")
	else:
		email = request.form['email']
		password = request.form['password']
		if check_login_credentials(username, password):
			return redirect(url_for('index'))
		else:
			return redirect(url_for('login'))

@webapp.route('/logout')
@check_loggied_in
def logout():
	"""
	Logs users out. Deletes the current session.
	Returns:
		Redirect - redirects to the login page.
	"""
	session.pop('logged-in', None)
	session.pop('email', None)
	session.pop('name', None)
	return redirect(url_for('login'))

@webapp.route('/create_new_user', methods=["POST"])
def create_new_user():
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	mongo = MyMongo()
	user_id = mongo.create_user(name, email, password)
	return user_id


def check_login_credentials(email, password):
	"""
	Checks if the user exists in the users file. Matches password and usernames to the
	ones found in the file. Creates a session if the user is successful at logging in.
	Parameters:
		username
		password
	Returns
		True - if user and passwords match 
		False - if user not found or password doesn't match
	"""
	#get user list
	users_list = get_users_as_list()
	for user_dict in users_list:
		if user_dict.__getitem__("email") == email and user_dict.__getitem__("password") == password:
			session['logged-in'] = True
			session['email'] = email
			session['name'] = name
			return True
	return False

def is_empty(any_structure):
	"""
	Simple helper function to help determin if a data
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


#If it's run directly by the python web system, start it
if __name__ == '__main__':
	#the secret key to encrypt and decrypt cookies
	webapp.secret_key = b'_0\xa5L\x0e\xd3"f\xfe\xbb\x07\xee\xebB?@\xaf.\xa6\xf0\xec\x19\x92\x95\xe6\xb2\xb4\xd1[ \xfad\x8bh\x93\xbf<b\xa5\xccV\xa4$%K4\xa8\xc4'
	webapp.run(host = _HOST, debug = _DEBUG, port = _PORT)
#We do that because if we use app engine or tornado server
#it calls it automatically, and uses different ports and namespaces