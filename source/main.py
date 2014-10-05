# Main
# Handles the homepage, welcome and "404" pages

#Import required modules
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import datetime
import os
import useragent

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
			#Uncomment to allow serving a "mobile" site to mobile users
			#if useragent.checkMobile(self.request):
				#template = JINJA_ENVIRONMENT.get_template('templates/homepage-mobile.html')
			#else:
			template = JINJA_ENVIRONMENT.get_template('templates/homepage.html')
			self.response.write(template.render({'user_nickname':user.nickname(), 'auth_url':auth_url}))


class NotFoundHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/notfound.html')
		self.response.write(template.render({'bad_uri':self.request.uri}))

app = webapp2.WSGIApplication([
	('/', HomePageHandler),
	('.*', NotFoundHandler)], 
	debug=True)
