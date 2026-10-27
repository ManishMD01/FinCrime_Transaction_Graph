# BigQuery Setup Guide

## Quick Start

### 1. Set up environment variables
Copy `.env.example` to `.env` and update with your values:
```bash
cp bigquery/config/.env.example bigquery/config/.env
```

Edit `bigquery/config/.env`:
```bash
GCP_PROJECT_ID=your-actual-project-id
BQ_DATASET_ID=fincrime_er
BQ_LOCATION=US
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create BigQuery dataset and tables
```bash
# Create dataset
bq mk --dataset --location=US your-project-id:fincrime_er

# Run DDL scripts (update project ID first or use env vars)
export GCP_PROJECT_ID=your-project-id
python bigquery/etl/setup_bigquery.py
```

### 4. Load historical data
```bash
python bigquery/etl/load_historical_data.py --customers data/customers.csv --transactions data/transactions.csv
```

### 5. Set up ETL for new data
```bash
python bigquery/etl/load_new_data.py --mode stream
```

## Configuration Files

| File | Purpose |
|------|---------|
| `config/.env` | Environment variables (create from .env.example) |
| `config/config.yaml` | YAML configuration with all settings |
| `config/config.py` | Python config loader |
| `config/bq_config.json` | JSON config for backward compatibility |

## Using the Config

### In Python
```python
from bigquery.config.config import config

# Get project details
print(config.project_id)
print(config.get_full_table_id('raw_customers'))
```

### In Shell Scripts
```bash
source bigquery/config/.env
bq query --use_legacy_sql=false --project_id=$GCP_PROJECT_ID < bigquery/ddl/01_create_raw_tables.sql
```

## Updating Project ID

To change project ID across all files:
1. Update `bigquery/config/.env` - main source
2. Or update `bigquery/config/config.yaml`
3. The Python code will read from environment variables automatically

All SQL files use placeholder `your-project-id` - use the setup script to replace them with your actual project ID.
