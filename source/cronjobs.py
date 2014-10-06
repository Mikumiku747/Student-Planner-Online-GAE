#Cronjobs
#Handles automated scheduled events, such as the deletion of past events and switching between weeks a and b.

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2

from timetable import Timetable

class WeekSwitchingScript(webapp2.RequestHandler):
	def get(self):
		tables = Timetable.query().fetch()
		for table in tables:
			table.isweeka = not table.isweeka
			table.put()
		
app = webapp2.WSGIApplication([
	('/admin/weekswitch', WeekSwitchingScript)], 
	debug=True)
