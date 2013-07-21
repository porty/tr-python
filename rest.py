import urllib
import urllib2
import json

'''
A simple REST class

@author Robert McNeil
'''
class Rest:
	def __init__(self, baseurl = ""):
		self.baseurl = baseurl

	def get(self, url = ""):
		return urllib2.urlopen(self.baseurl + url).read()

	def __post(self, url, data):
		data_str = urllib.urlencode(data)
		return urllib2.urlopen(self.baseurl + url, data_str).read()

	def post(self, url = "", **data):
		self.__post(url, data)

	def jget(self, url = ""):
		return json.loads(self.get(url))

	def jpost(self, url = "", **data):
		return json.loads(self.__post(url, data))
