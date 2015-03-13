#!/usr/bin/python
import requests
import re


class Resource(object):

	def __init__(self,name,uri,token):
		#make call for resource details
		print uri, token, name
		# r = requests.get(uri,headers={'x-auth-token':token})
		# res = r.json()

		# self._name = name;
		# self._token = token;
		# self._uri = uri;
		# self._method = res["method"]
		# self._description = res["description"];
		# self._required = []
		# self._optional = res["optional"]

	def _call(self,method="get",params={}):
		# replace url params
		url = self._uri
		matches = re.findall(r'\{(\S+?)\}',url)
		for m in matches:
			if m in params:
				url = re.sub('\{'+m+'\}',params[m],url)
				print url
		# remove all keys from dict used in url params

		# generate querystring
		
		# r = requests.get(url,params=params,headers={'x-auth-token':self._token})
		# res = res.json()
		# return res
		return "res"