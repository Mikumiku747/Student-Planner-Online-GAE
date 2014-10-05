# Timetable
# Handles showing, editing and creation of people's timetable

#Import required modules
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import datetime
import os

#Setup Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class ShowTimeTableHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/timetable.html')
		self.response.write(template.render())

app = webapp2.WSGIApplication([
	('/timetable', ShowTimeTableHandler)], 
	debug=True)
