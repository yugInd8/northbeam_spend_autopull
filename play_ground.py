#a script to test bunch of things on the northbeam api. Most of this is commented. But ignore this as whatever useful comes out from here is transferred into a new standalone script.
import requests
import time

def get_attribution_models(api_key, client_id):
    url = "https://api.northbeam.io/v1/exports/attribution-models"
    headers = {
        "accept": "application/json",
        "Authorization": api_key,
        "Data-Client-ID": client_id
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_metrics(api_key, client_id):
    url = "https://api.northbeam.io/v1/exports/metrics"
    headers = {
        "accept": "application/json",
        "Authorization": api_key,
        "Data-Client-ID": client_id
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_breakdowns(api_key, client_id):
    url = "https://api.northbeam.io/v1/exports/breakdowns"
    headers = {
        "accept": "application/json",
        "Authorization": api_key,
        "Data-Client-ID": client_id
    }
    response = requests.get(url, headers=headers)
    return response.json()

def create_data_export(api_key, client_id, payload):
    url = "https://api.northbeam.io/v1/exports/data-export"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": api_key,
        "Data-Client-ID": client_id
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def check_export_status(api_key, client_id, export_id):
    url = f"https://api.northbeam.io/v1/exports/data-export/result/{export_id}"
    headers = {
        "accept": "application/json",
        "Authorization": api_key,
        "Data-Client-ID": client_id
    }
    response = requests.get(url, headers=headers)
    return response.json()

def download_export_file(file_url):
    response = requests.get(file_url)
    with open('exported_data.csv', 'wb') as file:
        file.write(response.content)

def main(api_key, client_id):
    # Fetch available models, metrics, and breakdowns
    attribution_models = get_attribution_models(api_key, client_id)
    metrics = get_metrics(api_key, client_id)
    breakdowns = get_breakdowns(api_key, client_id)

    # #to understand the att models, metrics and breakdown options available
    # print("Attribution Models:", attribution_models)
    # print("=================================================================================================\n")
    # print("Metrics:", metrics)
    # print("=================================================================================================\n")
    # print("Breakdowns:", breakdowns)
    # print("=================================================================================================\n")

    # Defined an example of the payload for data export
    payload = {
        "level": "ad",
        "time_granularity": "DAILY",
        "period_type": "YESTERDAY",
        "breakdowns": [
            {
                "key": "Platform (Northbeam)",
                "values": ["Google Ads", "Facebook Ads", "TikTok"]
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
            "attribution_models": ["northbeam_custom__va"],
            "accounting_modes": ["accrual", "cash"],
            "attribution_windows": ["1"]
        },
        "metrics": [
            {"id": "spend", "label": "yesterday_spend"},
            {"id": "cpm"},
            {"id": "rev"}
        ]
    }

    export_response = create_data_export(api_key, client_id, payload)
    export_id = export_response.get("id")

    if export_id:
        print(f"Export ID: {export_id}")

        # Check export status and download result
        while True:
            status_response = check_export_status(api_key, client_id, export_id)
            status = status_response.get("status")
            if status == "SUCCESS":
                file_url = status_response.get("result")[0]
                download_export_file(file_url)
                print("Export file downloaded successfully.")
                break
            elif status == "FAILED":
                print("Export failed.")
                break
            else:
                #sometimes the export is being created and so might take some time
                print("Export in progress, checking again in 10 seconds...")
                time.sleep(10)
    else:
        print("Failed to create data export.")

if __name__ == "__main__":
    API_KEY = "your api key"
    CLIENT_ID = "your data client id"
    main(API_KEY, CLIENT_ID)
