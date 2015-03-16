#!/usr/bin/python
import requests
import re

class StrapResponse(object):

	def __init__(self,data=None,error=None):
		self.data = data
		self.error = error

	def setData(self,data):
		self.data = data

	def setError(self,err):
		self.error = error


class Resource(object):

	def __init__(self,name,json,token):
		self._name = name;
		self._token = token;
		self._uri = json["uri"][:]
		# self._uri = json["uri"].encode('utf-8');
		self._method = json["method"]
		self._description = json["description"];
		self._optional = set(json["optional"])

	def call(self,method="get",params=None):
		if params == None:
			params = {}

		# replace url params
		url = self._uri
		matches = re.findall(r'\{(\S+?)\}',url)
		for m in matches:
			if m in params:
				url = re.sub('\{'+m+'\}',params[m],url)
				# remove url param from rest of params 
				params.pop(m,None)

		# build list of items to be removed from querystring
		toRemove = [ p for p in params if p not in self._optional ]

		# remove all invalid items from querystring
		filter(lambda p: params.pop(p,None),toRemove)

		r = requests.get(url=url,params=params,headers={'x-auth-token':self._token})
		
		return self._package_error_with_data(r.json())

	def _package_error_with_data(self,res=None):
		if res == None:
			res = ""

		rv = StrapResponse(res)
		if "success" in res:
			if res["success"] == False:
				rv.setError(res)
		return rv
		
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
