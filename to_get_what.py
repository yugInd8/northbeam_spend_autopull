# This script helps understand what fields you might want. what keys etc for the paylod.

import requests
import json

# to list metrics or the attribution models or breakdowns present for you, use one of the following

#url = "https://api.northbeam.io/v1/exports/metrics"; filler="metrics"
url = "https://api.northbeam.io/v1/exports/attribution-models"; filler="attribution_models"
#url = "https://api.northbeam.io/v1/exports/breakdowns"; filler="breakdowns"

# get the api key and cliend data id from your northbeam account
API_KEY = "your unique api-key"
CLIENT_ID = "your data-client-id"

headers = {
    "accept": "application/json",
    "Authorization": API_KEY,
    "Data-Client-ID": CLIENT_ID
}

response = requests.get(url, headers=headers)
file_path = "data_{}.txt".format(filler)

if response.status_code == 200:
    data = response.json()
    
    # writing the flattened json to be readable
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
else:
    # 200 is success, 401 is unauthorised req, 429 is too many requests, 500 is a server error
    print(f"Request failed with status code {response.status_code}")
