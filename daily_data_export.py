# here we download the aggrigate data of needed platform for a single day. A metadata table tells the last ran date and a new run of the script downloads data for the next date. Refer the readme for better explanation.
import requests
import csv
import time
from datetime import datetime, timedelta
import os

API_URL = 'https://api.northbeam.io/v1/exports/data-export'

# Variables to be modified as you need. 
DATA_CLIENT_ID = 'data-client-id'
API_KEY = 'unique nb-api-key'
# Refer to 'to_get_what.py' script to know what attribution models and platforms are there. Platforms be listed under breakdown somewhere
ATTRIBUTION_MODEL = 'last_touch'
PLATFORMS = ['Google Ads', 'Facebook Ads', 'TikTok', 'Amazon - Ads and Organic', 'YouTube Ads']
# a variable for naming the output
CLIENT_NAME = "viome"

#the csv with metadat for last ran date
META_DATA_FILE = 'meta_d.csv'

HEADERS = {
    'Authorization': API_KEY,
    'Data-Client-ID': DATA_CLIENT_ID,
    'Content-Type': 'application/json',
}

class MetadataManager:
    def __init__(self, meta_file):
        self.meta_file = meta_file
        self._initialize_metadata()

    def _initialize_metadata(self):
        if not os.path.exists(self.meta_file):
            with open(self.meta_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['last_fetched_date', 'success'])

    def get_last_fetched_date(self):
        try:
            with open(self.meta_file, 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in reversed(rows):
                    if row.get('success') == 'SUCCESS':
                        return row['last_fetched_date']
        except Exception as e:
            print(f"Error reading metadata file: {e}")
        return None

    def update_metadata(self, date_fetched, success):
        with open(self.meta_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date_fetched, success])


# some utility functions
def determine_fetch_dates(metadata_manager):
    last_fetched = metadata_manager.get_last_fetched_date()

    if last_fetched:
        period_start = datetime.strptime(last_fetched, '%Y-%m-%d') + timedelta(days=1)
    else:
        period_start = datetime(datetime.now().year, 1, 1)

    period_end = period_start
    return period_start, period_end


def format_date_for_api(date_obj):
    return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')


# northBeam api interaction
class NorthbeamAPI:
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.headers = headers

    def initiate_export(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()

    def check_export_status(self, export_id):
        status_url = f"https://api.northbeam.io/v1/exports/data-export/result/{export_id}"
        status_response = requests.get(status_url, headers=self.headers)
        return status_response.json()

    def download_export_file(self, file_url, csv_filename):
        export_file = requests.get(file_url)
        with open(csv_filename, 'wb') as file:
            file.write(export_file.content)
        print(f"CSV file '{csv_filename}' has been downloaded successfully.")


class ExportManager:
    def __init__(self, api, metadata_manager):
        self.api = api
        self.metadata_manager = metadata_manager

    def create_payload(self, period_start, period_end):
        return {
            "level": "platform",
            "time_granularity": "DAILY",
            "period_type": "FIXED",
            "period_options": {
                "period_starting_at": format_date_for_api(period_start),
                "period_ending_at": format_date_for_api(period_end + timedelta(hours=23, minutes=59, seconds=59))
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

    def fetch_export_data(self, period_start, period_end):
        payload = self.create_payload(period_start, period_end)
        data = self.api.initiate_export(payload)
        export_id = data.get("id")

        if export_id:
            self.poll_export_status(export_id, period_start)
        else:
            print(f"Failed to initiate export. Error: {data}")

    def poll_export_status(self, export_id, period_start):
        while True:
            status_data = self.api.check_export_status(export_id)

            if status_data.get("status") == "SUCCESS":
                file_url = status_data.get("result")[0]
                csv_filename = f"{CLIENT_NAME}_spend_{period_start.strftime('%Y-%m-%d')}.csv"
                self.api.download_export_file(file_url, csv_filename)
                self.metadata_manager.update_metadata(period_start.strftime('%Y-%m-%d'), 'SUCCESS')
                break
            elif status_data.get("status") == "FAILED":
                print("Export failed.")
                self.metadata_manager.update_metadata(period_start.strftime('%Y-%m-%d'), 'FAILED')
                break
            else:
                print("Export in progress, checking again in 10 seconds...")
                time.sleep(10)

def main():
    # first off, initialize metadata and API manager
    metadata_manager = MetadataManager(META_DATA_FILE)
    northbeam_api = NorthbeamAPI(API_URL, HEADERS)

    # gets the next period_start and period_end dates
    period_start, period_end = determine_fetch_dates(metadata_manager)

    #a check so we dont try fetching future's data
    today = datetime.now().date()
    if period_start.date() >= today:
        print("Data directory is up to date.")
        return

    # debugging information
    print(f"Period Start: {period_start.strftime('%Y-%m-%d')}, Period End: {period_end.strftime('%Y-%m-%d')}")

    # fetching and downloading
    export_manager = ExportManager(northbeam_api, metadata_manager)
    export_manager.fetch_export_data(period_start, period_end)


if __name__ == "__main__":
    main()
