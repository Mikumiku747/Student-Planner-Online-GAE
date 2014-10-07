#Event
#Handles the creation, modification, showing and deletion of events by thier key. 

#Import required modules
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import datetime
import os
import time

#Setup Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#Model for events
class Event(ndb.Model):
	"Models an event"
	owner = ndb.UserProperty()
	name = ndb.StringProperty()
	type = ndb.StringProperty()
	description = ndb.StringProperty(indexed=False)
	when = ndb.DateTimeProperty(auto_now_add=True)
	
daycards = {'1':'st', '2':'nd', '3':'rd', '4':'th', '5':'th', '6':'th', '7':'th', '8':'th', '9':'th', '0':'th'}
weekdaycards = {0:'Monday', 1:"Tuesday", 2:"Wedneday", 3:"Thurday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
monthcards = {1:"January", 2:"Feburary", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}


def formatted_datetime(datetime_obj):
	result = weekdaycards[datetime_obj.weekday()]
	result = result + " the " 
	if len(str(datetime_obj.day))>1:
		result = result + str(datetime_obj.day)+daycards[str(datetime_obj.day)[1]]
	else:
		result = result + str(datetime_obj.day)+daycards[str(datetime_obj.day)[0]]
	result = result + " of "
	result = result + monthcards[datetime_obj.month]
	result = result + " at " + str(datetime_obj.time())[:5]
	return result

class ShowEventHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		typefilter = self.request.get("typefilter")
		if typefilter == "":
			eventlist = Event.query(Event.owner == user).order(Event.when).fetch()
		else:
			eventlist = Event.query(Event.owner == user, Event.type==typefilter).fetch()
		template = JINJA_ENVIRONMENT.get_template('templates/eventview.html')
		self.response.write(template.render({'typefilterword':typefilter, 'eventlist':eventlist, 'prettydatetime':formatted_datetime}))

class CreateEventHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		new_event = Event()
		new_event.owner = user
		new_event.name = "Event Name"
		new_event.type = ""
		new_event.description = "A short description of the event."
		event_key = new_event.put().urlsafe()
		time.sleep(1) #Give the event time to publish]
		self.redirect("/editevent?key={}".format(event_key))
		
class EditEventHandler(webapp2.RequestHandler):
	def get(self):
		target_event=ndb.Key(urlsafe=self.request.get('key')).get()
		template = JINJA_ENVIRONMENT.get_template('templates/editevent.html')
		self.response.write(template.render({'eventkey':self.request.get('key'), 'eventname':target_event.name, 'eventtype':target_event.type, 'eventwhendate':str(target_event.when.date()), 'eventwhentime':str(target_event.when.time()).split('.')[0], 'eventdescription':target_event.description}))
		
	def post(self):
		keystring = self.request.get('sharekey')
		target_event = ndb.Key(urlsafe=keystring).get()
		target_event.name = self.request.get('name')
		target_event.type = self.request.get('type')
		target_event.description = self.request.get('description')
		datewhen = self.request.get('datewhen')
		timewhen = self.request.get("timewhen")
		target_event.when = datetime.datetime(int(datewhen[0:4]), int(datewhen[5:7]), int(datewhen[8:10]), int(timewhen[0:2]), int(timewhen[3:5]))
		target_event.put()
		time.sleep(1)
		self.redirect("/event")
		
	
class DeleteEventHandler(webapp2.RequestHandler):
	def get(self):
		killkey = self.request.get("key")
		ndb.Key(urlsafe=killkey).delete()
		time.sleep(1)
		self.redirect("/event")
	
app = webapp2.WSGIApplication([
	('/event', ShowEventHandler),
	('/createevent', CreateEventHandler),
	('/editevent', EditEventHandler),
	('/deleteevent', DeleteEventHandler)], 
	debug=True)

