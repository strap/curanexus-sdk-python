# strapSDK

Strap SDK python provides an easy to use, chainable API for interacting with our API services. Its purpose is to abstract away resource information from our primary API, i.e. not having to manually track API information for your custom API endpoint.

Strap SDK python keys off of a global API discovery object using the read token for the API. The Strap SDK python extracts the need for developers to know, manage, and integrate the API endpoints.

The a Project API discovery can be found here:

HEADERS: "X-Auth-Token": GET https://api2.straphq.com/discover

Once the above has been fetched, strapSDK will fetch the API discover endpoint for the project and build its API.

### Installation

```
git clone git@github.com:strap/strap-sdk-python.git
```

### Usage
```python
  from strap-sdk-python import StrapSDK

  // initialize Strap SDK with read token
  strap = StrapSDK("QNIODsXElu3W7Csg452ge212GWQ0zjS2W3")
 
  // fill dict with url parameters and/or http request body key-value pairs
  params["someKey"] = "someValue"
 
  // make request for data based on params
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
```

