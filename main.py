from StrapSDK import StrapSDK

# initialize Strap SDK with read token
strap = StrapSDK("QNIODsZ4pPRbeLlEsXElu3W7C0zjS2W3")
if not strap.hasError():
	# fill dict with url parameters and/or http request body key-value pairs
	params = {}
	params["guid"] = "brian-strap"
	params["id"] = "PY0XxPm3i7FGQj3KweCpn8xCh"

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