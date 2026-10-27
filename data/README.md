# Data Directory

This directory manages data files for the ETL process with clear separation of loaded and unloaded files.

## Directory Structure

```
data/
├── incoming/   # Drop new CSV files here for processing
├── loaded/     # Successfully loaded files (moved here automatically)
├── unloaded/   # Files that couldn't be processed (wrong naming/type)
├── rejected/   # Files that failed validation
└── reference_data/ # Reference/lookup data
```

## Usage

### 1. Drop files in incoming/
Place your CSV files in `data/incoming/`. Name them with `customer` or `transaction` in the filename:
- `customers_2024_01.csv`
- `daily_transactions.csv`

### 2. Run ETL processor
```bash
cd /path/to/FinCrime_Transaction_Graph
source venv/bin/activate
python bigquery/etl/load_with_validation.py
```

### 3. Check results
- **loaded/** - Successfully processed and loaded to BigQuery
- **rejected/** - Failed validation (check errors in logs)
- **unloaded/** - Unrecognized file type
- **incoming/** - Should be empty after processing

## Features

- **Duplicate Prevention** - Checks file hash against already loaded files
- **Validation** - Validates required columns, data types, duplicates
- **File Tracking** - All files tracked in `etl_file_tracking` table
- **Auto-Movement** - Files moved to appropriate directories
- **Batch Tracking** - Each run gets a unique batch ID
