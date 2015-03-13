#!/usr/bin/python
import requests
from Resource import Resource

class StrapSDK(object):

	def __init__(self, token):
		self._discoveryURL = "https://api2.straphq.com/discover"
		self._token = token
		self._resources = self._discover()
		self._error = ""

	def _discover(self):
		headers = {'x-auth-token': self._token}
		r = requests.get(self._discoveryURL, headers=headers)

		# create resource objects out of each service url
		services = r.json()
		for s in services:
			r = Resource(s, services[s], self._token)
			self._resources[s] = r

	def _call(self, serviceName, method="get", params={}):
		return self._resources[serviceName].call(method, params)

	def getActivity(self, params={}):
		return self._call("activity", params)

	def getToday(self, params={}):
		return self._call("today", params)

	def getUsers(self, params={}):
		return self._call("users", params)

	def getReport(self, params={}):
		return self._call("report", params)

	def getTrigger(self, params={}):
		return self._call("trigger", params)

if __name__ == '__main__':
	strap = StrapSDK("hBp4e7HG7KGWJr16OP2HXykw0gaGJY8i")
	strap.getActivity()
