# Timetable
# Handles showing, editing and creation of people's timetable

#Import required modules
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import datetime
import os
import json
import time

#Setup Jinja2
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

#NDB model for a timetable
class Timetable(ndb.Model):
	owner = ndb.UserProperty()
	weeka = ndb.StringProperty(indexed=False) #Store each week as a JSON encoded string
	weekb = ndb.StringProperty(indexed=False) #so we don't have a bazillion properties.
	isweeka = ndb.BooleanProperty() #Keep track of which week it is


class ShowTimeTableHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		users_table = Timetable.query(Timetable.owner == user).fetch(1) #Gets the first TimeTable to pop up for this user
		if len(users_table)==0:
			self.response.write('<h3>You have not made a timetable yet!</h3><p>You can set one up whenever you want, just click <a href="createtimetable" target="_parent">here</a> to make one.')
		else:
			table = users_table[0]
			template = JINJA_ENVIRONMENT.get_template('templates/timetable.html')
			self.response.write(template.render({'isweeka':table.isweeka, 'dataa':json.loads(table.weeka), 'datab':json.loads(table.weekb)}))

class CreateTimeTableHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		new_table = Timetable()
		new_table.owner = user
		new_table.isweeka = True
		
		#Provide somee default lists to populate the timetable with
		weeka = [[['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Sport / Free period', '', ''], ['Sport / Free period', '', '']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']]]
		weekb = [[['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Sport / Free period', '', ''], ['Sport / Free period', '', '']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']], [['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location'], ['Subject', 'Teacher', 'Location']]]
		
		new_table.weeka = json.dumps(weeka)
		new_table.weekb = json.dumps(weeka)
		
		#Publish the new table to the datastore, and verify it was stored before redirecting.
		new_table.put()
		time.sleep(1) #Let it publish
		while len(Timetable.query(Timetable.owner == user).fetch())<=0:
			pass #Verify it published
		self.redirect("/edittimetable")
		
class EditTimeTableHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		table = Timetable.query(Timetable.owner==user).fetch(1) #Grab the user's first timetable
		if len(table)<=0:
			self.response.write("""<h2>Error: We couldn't find your timetable</h2><p>Please head to the homepage or <a href="/createtimetable">click here</a> to create one.</p>""")
		else:
			table = table[0]
			weeka = json.loads(table.weeka)
			weekb = json.loads(table.weekb)
			template = JINJA_ENVIRONMENT.get_template('templates/edittimetable.html')
			self.response.write(template.render({'isweeka':table.isweeka, 'weekadata':weeka, 'weekbdata':weekb, 'nickname':user.nickname()}))
	
	def post(self):
		#Construct the timetable from the POST data
		weeka = []
		weekb = []
		isweeka = self.request.get('week')
		for week in ["A", "B"]:
			for day in ["MON", "TUE", "WED", "THU", "FRI"]:
				new_day = []
				for lesson in ["1", "2", "3", "4"]:
					new_lesson = []
					for field in ["S", "T", "L"]:
						new_field=self.request.get(str(week+day+lesson+field))
						new_lesson.append(new_field)
					new_day.append(new_lesson)
				if week=="A":
					weeka.append(new_day)
				else:
					weekb.append(new_day)
		
		user = users.get_current_user()
		
		table = Timetable.query(Timetable.owner==user).fetch(1)[0] #Directly grab the user's timetable
		table.weeka = json.dumps(weeka)
		table.weekb = json.dumps(weekb)
		if self.request.get('week')=='a':
			table.isweeka = True
		else:
			table.isweeka = False
		table.put()
		time.sleep(1) #Give it time to publish
		self.redirect('/')
		
		
			

app = webapp2.WSGIApplication([
	('/timetable', ShowTimeTableHandler),
	('/createtimetable', CreateTimeTableHandler),
	('/edittimetable', EditTimeTableHandler)], 
	debug=True)
