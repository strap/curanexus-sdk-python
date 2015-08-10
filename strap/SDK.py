#!/usr/bin/python
import requests, re, json

class StrapResponse(object):

    def __init__(self,data=None,error=None):
        self.data = data
        self.error = error

    def setData(self,data):
        self.data = data

    def setError(self,error):
        self.error = error


class Resource(object):

    def __init__(self,name,json,token):

        self._name = name;
        self._token = token;
        self._uri = json["uri"]
        # self._uri = json["uri"].encode('utf-8');
        self._method = json["method"]
        self._description = json["description"];

        if "optional" in json:
            self._optional = set(json["optional"])
        else:
            self._optional = set()

    def call(self, params={}, data={}):

        # Construct url
        url = self._constructUrl(params)

        # build list of items to be removed from querystring
        toRemove = [ p for p in params if p not in self._optional ]

        # remove all invalid items from querystring
        filter(lambda p: params.pop(p,None),toRemove)

        if self._method == "POST":
            return self._post(url, params, data)
        elif self._method == "PUT":
            return self._put(url, params, data)
        elif self._method == "DELETE":
            return self._delete(url, params)
        else:
            return self._get(url, params)

    def _get(self, url, params):

        r = requests.get(url=url, params=params, headers={'x-auth-token':self._token})

        return self._package_error_with_data(r.json())

    def _post(self, url, params, data):

        r = requests.post(url=url, params=params, data=json.dumps(data), headers={'x-auth-token':self._token})

        return self._package_error_with_data(r.json())


    def _put(self, url, params, data):

        r = requests.put(url=url, params=params, data=json.dumps(data), headers={'x-auth-token':self._token})

        return self._package_error_with_data(r.json())


    def _delete(self, url, params):

        r = requests.delete(url=url, params=params, headers={'x-auth-token':self._token})

        if len(r.text):
            return self._package_error_with_data(r.json())
        else:
            return {}

    def _constructUrl(self, params):
        # replace url params
        url = self._uri
        matches = re.findall(r'\{(\S+?)\}',url)
        for m in matches:
            if m in params:
                url = re.sub('\{'+m+'\}',params[m],url)
                # remove url param from rest of params
                params.pop(m,None)
            else:
                url = re.sub('\{'+m+'\}(\/)?', '', url)

        return url

    def _package_error_with_data(self,res=""):

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
        resources = {}

        for service in res:
            for req in res[service]:
                if not req["method"] in resources:
                    resources[req["method"]] = {}

                resources[req["method"]][service] = Resource(service, req, self._token)

        return resources

    def hasError(self):
        rv = False
        if self.error:
            rv = True
        return rv

    def getActivity(self, params={}):
        return self._resources["GET"]["activity"].call(params)

    def getToday(self, params={}):
        return self._resources["GET"]["today"].call(params)

    def getUsers(self, params={}):
        return self._resources["GET"]["users"].call(params)

    def getReport(self, params={}):
        return self._resources["GET"]["report"].call(params)

    def getTrigger(self, params={}):
        return self._resources["GET"]["trigger"].call(params)

    def getJobs(self, params={}):
        return self._resources["GET"]["job"].call(params)

    def getBehavior(self, params={'guid': 'none'}):
        return self._resources["GET"]["behavior"].call(params)

    def getSegmentations(self, params={}):
        return self._resources["GET"]["segmentation"].call(params)

    def getReportDetails(self, params={'id': 'none'}):
        return self._resources["GET"]["raw"].call(params)

    def createJob(self, data={}):
        return self._resources["POST"]["job"].call({}, data);

    def updateJob(self, params={}, data={}):
        return self._resources["PUT"]["job"].call(params, data);

    def deleteJob(self, params={}):
        return self._resources["DELETE"]["job"].call(params);
