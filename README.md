# Python > Strap Server-Side SDK

Strap SDK python provides an easy to use, chainable API for interacting with our API services. Its purpose is to abstract away resource information from our primary API, i.e. not having to manually track API information for your custom API endpoint.

Strap SDK python keys off of a global API discovery object using the read token for the API. The Strap SDK python extracts the need for developers to know, manage, and integrate the API endpoints.

The a Project API discovery can be found here:

HEADERS: "X-Auth-Token": GET https://api2.straphq.com/discover

Once the above has been fetched, strapSDK will fetch the API discover endpoint for the project and build its API.

### Installation

```
curl -O https://s3.amazonaws.com/strap-sdk/strap-sdk-python.tar.gz
pip install strap-sdk-python.tar.gz
```

### Usage
```python
from strap.SDK import StrapSDK

# initialize Strap SDK with read token
strap = StrapSDK("ReadToken")
if not strap.hasError():
  # fill dict with url parameters and/or http request body key-value pairs
  params = {}
  params["guid"] = "yourGuid"
  params["id"] = "ID of activity"

  # make request for data based on params
  activities = strap.getActivity(params)
  print activities.data
  print activities.error

  today = strap.getToday(params)
  print today.data
  print today.error

  users = strap.getUsers(params)
  print users.data
  print users.error

  report = strap.getReport(params)
  print report.data
  print report.error

  trigger = strap.getTrigger(params)
  print trigger.data
  print trigger.error
else:
  print strap.error
```

