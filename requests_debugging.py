import requests


def requestURL(baseurl, params: dict):
    # This function accepts a URL path and a params diction as inputs.
    # It calls requests.get() with those inputs,
    # and returns the full URL of the data you want to get.
    req = requests.Request(method='GET', url=baseurl, params=params)
    prepped = req.prepare()
    return prepped.url
