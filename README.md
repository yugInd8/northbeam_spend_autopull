# Northbeam API Data Handler

This repository contains scripts to interact with Northbeam's API, fetching and aggregating data for various business purposes. Below is the setup guide and explanation of each script currently available.

## Setup

### Requirements

- Python 3.x
- Ensure you have your Northbeam `API_KEY` and `CLIENT_ID` from your Northbeam account.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yugInd8/northbeam_spend_autopull.git
   ```
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Scripts

### 1. **to_get_what.py**

This script helps you explore what fields, keys for the payload you might want to use while working with Northbeam API. It allows you to list available metrics, attribution models, or breakdowns.

**How to Use:**

1. Replace the placeholder API and client IDs with your actual values:
   ```python
   API_KEY = "your unique api-key"
   CLIENT_ID = "your data-client-id"
   ```
2. Uncomment the line for the specific data type you want to list (`metrics`, `attribution-models`, or `breakdowns`).

3. Run the script:
   ```bash
   python to_get_what.py
   ```

4. The result will be saved as a `.txt` file in a readable format based on the selection.

### 2. **aggregate_spend.py**

This script aggregates spend data across multiple platforms between a start and end date (defaulting to Jan 1, 2024, to today). It retrieves data such as spend amount, ROAS, AOV, and more, then outputs the results into a CSV file.

**How to Use:**

1. Update the following variables with your details:
   ```python
   DATA_CLIENT_ID = '<your unique data-client-id>'
   API_KEY = '<your unique api-key from Northbeam>'
   CLIENT_NAME = "your_client_name"
   period_start = 'YYYY-MM-DDT00:00:00Z'  # Update if necessary
   period_end = 'YYYY-MM-DDT00:00:00Z'  # Update if necessary
   ```
2. Customize the attribution model, platforms, and metrics as needed.

3. Run the script:
   ```bash
   python aggregate_spend.py
   ```

4. The output CSV will be saved as:
   ```
   {CLIENT_NAME}_spend_{start_date}_to_{end_date}.csv
   ```

### 3. **daily_data_export.py**

This script is designed to download aggregated data for a specific platforms for a single day. It maintains metadata about the last successful run, ensuring that each run fetches data for the next available day. This helps in automating the data fetching process and keeping the data up-to-date.

**How to Use:**

1. Update the following variables with your details:
   ```python
   DATA_CLIENT_ID = 'your-data-client-id'
   API_KEY = 'your-unique-api-key'
   CLIENT_NAME = "your_client_name"
   META_DATA_FILE = 'meta_d.csv'
   ```

2. Ensure that the metadata CSV file (`meta_d.csv`) is present in your working directory. This file will be created if it does not already exist.

3. Run the script:
   ```bash
   python daily_data_export.py
   ```

**Script Functionality:**

- **Metadata Management:** Maintains a CSV file (`meta_d.csv`) to keep track of the last fetched date and the success status of the export.
- **Determine Fetch Dates:** The next date for the last successful fetch date.
- **API Interaction:** 
  - Initiates a data export request to Northbeam’s API.
  - Polls the export status until the data is available.
  - Downloads the export file and saves it as a CSV.
- **Error Handling:** Updates the metadata with success or failure status based on the export process.

**Output:**

- A CSV file named `{CLIENT_NAME}_spend_{date}.csv` will be created with data for the specified day.
- The metadata CSV (`meta_d.csv`) will be updated with the date of the successful or failed fetch.

**Notes:**
- If the data directory is up to date, the script will notify you and exit without performing any new data fetch.

---

## Future Work

To make things more modular, the next stage on this repo's work has been pushed into a completely different repository. You can go ahead and read more more at :
https://github.com/yugInd8/aws_northbeam_pipeline

## Contributing

If you find any bugs or want to add new features, please create a pull request or raise an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

