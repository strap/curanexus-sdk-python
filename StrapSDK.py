#!/usr/bin/python
import requests
from Resource import Resource

class StrapSDK(object):

	def __init__(self, token):
		self.error = None
		self._discoveryURL = "https://api2.straphq.com/discover"
		self._token = token
		self._resources = self._discover()

	def _discover(self):
		# get resource list with descriptors
		r = requests.get(self._discoveryURL, headers={'x-auth-token': self._token})
		res = r.json()
		
		# return early if discovery failed
		if "success" in res:
			if res["success"] == False:
				self.error = res
				return None

		# create resource objects out of each service url
		services, resources = res, {}
		for s in services:
			resources[s] = Resource(s, services[s], self._token)
		return resources

	def hasError(self):
		rv = False
		if self.error:
			rv = True
		return rv

	def getActivity(self, params=None):
		if params == None:
			params = {}
		return self._resources["activity"].call("get", params)

	def getToday(self, params=None):
		if params == None:
			params = {} 
		return self._resources["today"].call("get", params)

	def getUsers(self, params=None):
		if params == None:
			params = {} 
		return self._resources["users"].call("get", params)

	def getReport(self, params=None):
		if params == None:
			params = {} 
		return self._resources["report"].call("get", params)

	def getTrigger(self, params=None):
		if params == None:
			params = {} 
		return self._resources["trigger"].call("get", params)
