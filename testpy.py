#!/usr/local/bin/python

import json
import requests

url = "http://www.sfu.ca/security/sfuroadconditions/api/3/current"
response = json.loads(requests.get(url).text)
# print(json.dumps(response, indent=4))
print(response["campuses"]["burnaby"]["roads"])