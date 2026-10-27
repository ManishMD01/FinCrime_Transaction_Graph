# Environment Migration Guide

When moving this project from one environment/GCP account to another, follow this guide.

## Pre-Migration Checklist
- [ ] Copy entire project directory to new environment
- [ ] Have new GCP service account key ready
- [ ] Have new GCP project ID
- [ ] Ensure BigQuery API is enabled in new project

## Migration Steps

### 1. Install Dependencies
```bash
cd /path/to/FinCrime_Transaction_Graph
./install/install.sh
```

### 2. Configure for New Environment
```bash
cd bigquery/config
cp .env.example .env
# Edit with new values
nano .env
```

Required values:
```env
GCP_PROJECT_ID=new-project-id
BQ_DATASET_ID=fincrime_er
BQ_LOCATION=US
GOOGLE_APPLICATION_CREDENTIALS=/path/to/new-service-account.json
ENVIRONMENT=prod
```

### 3. Setup BigQuery Resources
```bash
source ../../venv/bin/activate
python ../../bigquery/etl/setup_bigquery.py
```

This creates:
- Dataset in new project
- All raw/staging/resolved/graph/alerts tables
- Partitions and clustering
- Views

### 4. Migrate Data (Optional)
If you need data from old project:

**Export from old project:**
```bash
bq extract --destination_format CSV 'old-project:fincrime_er.raw_customers' gs://bucket/customers.csv
```

**Import to new project:**
```bash
python bigquery/etl/load_historical_data.py --customers data/customers.csv
```

### 5. Verify Installation
```bash
# Test config
python -c "from bigquery.config.config import config; print(config.project_id)"

# Test BigQuery connection
python -c "
from google.cloud import bigquery
from bigquery.config.config import config
client = bigquery.Client(project=config.project_id)
print('Connected to', config.project_id)
"
```

## What Changes Between Environments
- ✅ **Changes needed**: GCP project ID, service account key, dataset location (if different)
- ✅ **Auto-handled**: All table creation via setup script
- ✅ **No code changes**: Everything is environment-driven

## Troubleshooting
If tables already exist, setup script is idempotent and safe to re-run.
