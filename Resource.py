#!/usr/bin/python
import requests
import re

class Resource(object):

	def __init__(self,name,json,token):
		self._name = name;
		self._token = token;
		self._uri = json["uri"];
		self._method = json["method"]
		self._description = json["description"];
		self._required = []
		self._optional = json["optional"]

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
		
		# pass remaining params as querystring
		r = requests.get(url,params=params,headers={'x-auth-token':self._token})
		return package_error_with_data(r.json())

	def package_error_with_data(res):
		rv = {
			data : res,
			error : ""
		}
		if "success" in res:
			if res["success"] == false:
				rv["data"] = ""
				rv["error"] = res
		return rv