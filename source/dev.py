#Dev
# Handles some special development requests, mostly just  for 
# me debugging the application as I develop it. Think of this
# module as a sandpit, where I will make some temporary code to perform some special functions

import webapp2

class AgentHandler(webapp2.RequestHandler):
	def get(self):
		userAgent_raw = self.request.headers['User-Agent']
		agents_wlayout = userAgent_raw.split()
		agents = []
		for comp in agents_wlayout:
			if '/' in comp and not ("(" in comp or ")" in comp):
				agents.append(comp)
		self.response.write("<html>\nUser agent string: {}<br>".format(userAgent_raw))
		self.response.write("User agent components: {}<br>".format(agents))
		platforms = []
		versions = []
		for pair in agents:
			platforms.append(pair.split('/')[0])
			versions.append(pair.split('/')[1])
		self.response.write("Your user agents contains the following platforms:<br><ul>")
		for count in range(len(platforms)):
			self.response.write("<li>{name} - Version {ver}</li>".format(name=platforms[count], ver=versions[count]))
		deviceInfo = userAgent_raw[userAgent_raw.find('(')+1:userAgent_raw.find(')')]
		self.response.write("</ul>Browser device information: {info}<br>".format(info=deviceInfo))
		if "Android" in deviceInfo or "iPhone" in deviceInfo or "mobile" in deviceInfo:
			self.response.write("You are browsing on an android, ios or other mobile device.<br>")
		else:
			self.response.write("You are browsing on a desktop or other non-mobile device.<br>")
		self.response.write("</html>")

app = webapp2.WSGIApplication([
	('/dev/agent', AgentHandler)
	], debug=True)