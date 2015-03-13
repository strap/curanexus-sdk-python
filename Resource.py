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
		self._uri = json["uri"].encode('utf-8');
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

		# pass remaining valid params as querystring
		r = requests.get(url,params=params,headers={'x-auth-token':self._token})
		
		return self._package_error_with_data(r.json())

	def _package_error_with_data(self,res=None):
		if res == None:
			res = ""

		rv = StrapResponse(res)
		if "success" in res:
			if res["success"] == False:
				rv.setError(res)
		return rv