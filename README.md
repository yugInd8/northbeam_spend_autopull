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

---

## Future Work

As the repository grows, needed ways to handle the data from nb api will be included.
