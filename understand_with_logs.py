#this script ingests spends data from northbeam api but is essentially created for a developer to understand the responses and requests at each step by logs. Can be ignored.
import requests
import os
import json
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

url = "https://api.northbeam.io/v1/exports"
access_token = "<your unique access token>"  
DATA_CLIENT_ID = "your data client id" 
# source = "northbeam"
# feed = "spends"
PLATFORMS = ["Google Ads", "Facebook Ads", "TikTok", "Amazon - Ads and Organic", "YouTube Ads"]
ATTRIBUTION_MODEL = "last_touch"

# Specify the start date (modify as needed). Note : the northbeam API returns data for start and end date with inclusive limits. 
start_date = "2024-08-21T00:00:00Z"
end_date = (datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=23, minutes=59, seconds=59)).strftime("%Y-%m-%dT%H:%M:%SZ")

HEADERS = {
    'Authorization': access_token,
    'Data-Client-ID': DATA_CLIENT_ID,
    'Content-Type': 'application/json',
}

payload = {
    "level": "platform",
    "time_granularity": "DAILY",
    "period_type": "FIXED",
    "period_options": {
        "period_starting_at": start_date,
        "period_ending_at": end_date
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
        "aggregate_data": False,
        "include_ids": True,
        "include_kind_and_platform": True
    },
    "attribution_options": {
        "attribution_models": [ATTRIBUTION_MODEL],
        "accounting_modes": ["accrual"],
        "attribution_windows": ["1"]
    },
    "metrics": [
        {"id": "spend", "label": "spend_amount"},
        {"id": "aov", "label": "AOV"},
        {"id": "googleClicks", "label": "Google_Clicks"},
        {"id": "impressions", "label": "Imprs"},
        {"id": "metaLinkClicks", "label": "FB_Link_Clicks_Default"},
        {"id": "roas", "label": "ROAS"}
    ]
}

def initiate_export():
    endpoint = "data-export"
    export_url = f"{url}/{endpoint}"
    logger.info(f"Initiating export with URL: {export_url}\n")
    response = requests.post(export_url, headers=HEADERS, json=payload)
    logger.info(f"Response : {response} Type : {type(response)}\n")

    if response.status_code == 201:
        logger.info(f"API call successful: Initiating export. The export id generated should be here, in the response's json() : {response.json()}\n")
        logger.info(f"The other headers to our response : {response.headers}\n")
        return response.json()
    else:
        logger.error(f"API call failed: {response.status_code} {response.text}\n")
        return None

def poll_export_status(export_id):
    while True:
        endpoint = f"data-export/result/{export_id}"
        status_url = f"{url}/{endpoint}"
        status_response = requests.get(status_url, headers=HEADERS)

        if status_response.status_code == 200:
            logger.info("Polling export status successful.\n")
        else:
            logger.error(f"Failed to get export status: {status_response.status_code} {status_response.text}\n")
            return None

        status_data = status_response.json()
        logger.info(f"Status Data logs  : {status_data}")
        if status_data.get("status") == "SUCCESS":
            logger.info("Export successful.\n")
            file_url = status_data.get("result")[0]
            return file_url
        elif status_data.get("status") == "FAILED":
            logger.error("Export failed.\n")
            return None
        else:
            logger.info("Export in progress. Retrying in 10 seconds...")
            time.sleep(10)

def download_export_file(file_url, csv_filename):
    export_file = requests.get(file_url)
    with open(csv_filename, 'wb') as file:
        file.write(export_file.content)
    logger.info(f"CSV file '{csv_filename}' downloaded successfully.\n")

def main():
    logger.info("Starting Northbeam data fetch.\n")
    
    export_response = initiate_export()
    if not export_response:
        logger.error("Failed to initiate export.")
        return

    export_id = export_response.get("id")
    if not export_id:
        logger.error("No export ID received.")
        return

    file_url = poll_export_status(export_id)
    if not file_url:
        logger.error("Failed to retrieve file URL.")
        return

    csv_filename = "datasuch.csv"
    download_export_file(file_url, csv_filename)

if __name__ == "__main__":
    main()
