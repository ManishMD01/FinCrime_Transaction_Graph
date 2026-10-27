# ETL Quick Start Guide

## File-Based ETL with Validation

### Step 1: Prepare Files
Drop CSV files in `data/incoming/` with appropriate naming:
- `customers.csv` or `customer_data.csv`
- `transactions.csv` or `transaction_data.csv`

### Step 2: Run Validation & Load
```bash
cd /home/pritsingh000/Git/FinCrime_Transaction_Graph
source venv/bin/activate
python bigquery/etl/load_with_validation.py
```

### Step 3: Check Status
```bash
# View tracking in BigQuery
python -c "
from bigquery.config.config import config
from google.cloud import bigquery
client = bigquery.Client(project=config.project_id)
query = f'SELECT * FROM \`{config.get_dataset_ref()}.etl_file_tracking\` ORDER BY load_timestamp DESC LIMIT 10'
print(client.query(query).to_dataframe())
"
```

## Features

- **Prevents Duplicates**: Uses file hash to prevent loading same file twice
- **Validates Data**: Checks required columns, nulls, duplicates
- **Tracks Everything**: All files logged in BigQuery tracking tables
- **Organizes Files**: Auto-moves to loaded/unloaded/rejected directories
- **Batch Tracking**: Each load gets unique batch ID
