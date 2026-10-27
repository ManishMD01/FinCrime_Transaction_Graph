# Quick Start - BigQuery Configuration

## Step 1: Configure Your Project
```bash
cd bigquery/config
cp .env.example .env
```

Edit `.env` with your GCP details:
```env
GCP_PROJECT_ID=my-fincrime-project
BQ_DATASET_ID=fincrime_er
BQ_LOCATION=US
GOOGLE_APPLICATION_CREDENTIALS=/home/user/keys/service-account.json
ENVIRONMENT=dev
```

## Step 2: Setup BigQuery
```bash
# From project root
python bigquery/etl/setup_bigquery.py
```

This will:
- Create the dataset
- Create all tables (raw, staging, resolved, graph, alerts)
- Replace all placeholder project IDs automatically

## Step 3: Load Data

### Load Historical Data
```python
from bigquery.etl.load_historical_data import HistoricalDataLoader
loader = HistoricalDataLoader()
loader.load_customers_from_csv('data/historical_customers.csv')
loader.load_transactions_from_csv('data/historical_transactions.csv')
```

### Load New Data (ETL Process)
```python
from bigquery.etl.load_new_data import NewDataLoader
import pandas as pd

loader = NewDataLoader()
new_customers = pd.read_csv('incoming/customers.csv')
new_transactions = pd.read_csv('incoming/transactions.csv')
loader.load_new_customers(new_customers)
loader.load_new_transactions(new_transactions)
```

## Step 4: Run Entity Resolution with BigQuery
```python
from src.bigquery.bq_er_pipeline import BigQueryERPipeline

bq_er = BigQueryERPipeline(match_threshold=0.75)
resolved, golden = bq_er.run_with_historical_data(days_back=365)
# Results automatically written to BigQuery
```

## Notes
- All configuration is centralized in `bigquery/config/`
- No hardcoded project IDs in code - everything uses environment variables
- DDL scripts use placeholders that get replaced during setup
- Easy to switch between projects/environments by changing .env
