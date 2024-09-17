# this script aggregates spend data from a start date to end dat. Default : 1st Jan to today.

import requests
import csv
import time
from datetime import datetime

API_URL = 'https://api.northbeam.io/v1/exports/data-export'
# Variables to be modified as you need. 
DATA_CLIENT_ID = '<your unique data-client-id>'
API_KEY = '<you unique api-key from northbeam account>'
# Refer to 'to_get_what.py' script to know what attribution models and platforms are there. Platforms be listed under breakdown somewhere
ATTRIBUTION_MODEL = 'last_touch' 
PLATFORMS = ['Google Ads', 'Facebook Ads', 'TikTok', 'Amazon - Ads and Organic', 'YouTube Ads']
# a naming variable for output file
CLIENT_NAME = "viome"

# for dates. 
# note : THE API RETURNS AGGREGATED DATA FOR INCLUSIVE [a,b] limits
period_start = '2024-01-01T00:00:00Z' #chnage it as you want. this is the date from which the aggregation would start. Default set to 1st jan 2024
period_end = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') #today's

headers = {
    'Authorization': API_KEY,
    'Data-Client-ID': DATA_CLIENT_ID,
    'Content-Type': 'application/json',
}

payload = {
    "level": "platform",
    "time_granularity": "DAILY",
    "period_type": "FIXED",
    "period_options": {
        "period_starting_at": period_start,
        "period_ending_at": period_end
    },
    "breakdowns": [
        {
            "key": "Platform (Northbeam)",
            "values": PLATFORMS
        }
    ],
    "options": {
        "export_aggregation": "BREAKDOWN",
        "remove_zero_spend": False,
        "aggregate_data": True,
        "include_ids": False,
        "include_kind_and_platform": False
    },
    "attribution_options": {
        "attribution_models": [ATTRIBUTION_MODEL],
        "accounting_modes": ["accrual"], #"cash"],
        "attribution_windows": ["1"]
    },
    "metrics": [
        {"id": "spend", "label": "spend_amount"}, 
        {
            "id": "aov",
            "label": "AOV"
        },
        {
            "id": "googleClicks",
            "label": "Google_Clicks"
        },
        {
            "id": "impressions",
            "label": "Imprs"
        },
        {
            "id": "metaLinkClicks",
            "label": "FB_Link_Clicks_Default" 
        },
        {
            "id": "roas",
            "label": "ROAS"
        }
    ]
}

# the API request to initiate data export
response = requests.post(API_URL, headers=headers, json=payload)
data = response.json()

export_id = data.get("id")
if export_id:
    print(f"Export ID: {export_id}")

    # Polling for export status and downloads the result
    while True:
        status_url = f"https://api.northbeam.io/v1/exports/data-export/result/{export_id}"
        status_response = requests.get(status_url, headers=headers)
        status_data = status_response.json()

        if status_data.get("status") == "SUCCESS":
            file_url = status_data.get("result")[0]
            export_file = requests.get(file_url)

            # CSV file name format is : client_spend_endDate.csv
            date_onlyE = period_end.split('T')[0]
            date_onlyS = period_start.split('T')[0]
            csv_filename = f"{CLIENT_NAME}_spend_{date_onlyS}_to_{date_onlyE}.csv"

            with open(csv_filename, 'wb') as file:
                file.write(export_file.content)

            print(f"CSV file '{csv_filename}' has been downloaded successfully.")
            break
        elif status_data.get("status") == "FAILED":
            print("Export failed.")
            break
        else:
            print("Export in progress, checking again in 10 seconds...")
            time.sleep(10)
else:
    print(f"Failed to initiate export. Error: {data}")
