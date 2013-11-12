from flask import Flask, request, send_file, abort, make_response, session, escape, url_for, redirect, render_template

#Constants
_PORT = 9110
_HOST = '0.0.0.0' #this will find the current ip address and use it
_DEBUG = True

webapp = Flask(__name__)  #main namespace


@webapp.route('/')
def index():
	return "Hello mate"


@webapp.route('/signup', methods=["POST","GET"])
def request_become_member():
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		return "Usernme = {}, Password = {}".format(username,password)
	else:
		return render_template('signup.html')
	#Checkif user eixsts in user document in database
	#if yes
	#return error
	#if no
	#Add user to database




#If it's run directly by the python web system, start it
if __name__ == '__main__':
	#the secret key to encrypt and decrypt cookies
	webapp.secret_key = b'_0\xa5L\x0e\xd3"f\xfe\xbb\x07\xee\xebB?@\xaf.\xa6\xf0\xec\x19\x92\x95\xe6\xb2\xb4\xd1[ \xfad\x8bh\x93\xbf<b\xa5\xccV\xa4$%K4\xa8\xc4'
	webapp.run(host = _HOST, debug = _DEBUG, port = _PORT)
#We do that because if we use app engine or tornado server
#it calls it automatically, and uses different ports and namespaces