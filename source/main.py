# Main
# Handles the homepage, welcome and "404" pages

#Import required modules
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import datetime
import os

#Setup Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class HomePageHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if not user:
			auth_url = users.create_login_url("/")
			#Render a template and send it off to the user
			template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
			self.response.write(template.render({'auth_url':auth_url}))
		else:
			auth_url = users.create_logout_url("/")
			#Render a template and send it off to the user
			template = JINJA_ENVIRONMENT.get_template('templates/homepage.html')
			self.response.write(template.render({'user_nickname':user.nickname(), 'auth_url':auth_url}))

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect("/")
		

app = webapp2.WSGIApplication([
	('/', HomePageHandler)], 
	debug=True)
