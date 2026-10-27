# BigQuery Integration for FinCrime Entity Resolution Engine

This folder contains all BigQuery-related scripts, schemas, DDL/DML for table creation, and ETL utilities to support the FinCrime Entity Resolution Engine with Google BigQuery as the data warehouse.

## Overview

- **Historical Data**: Stored in BigQuery tables for scalable analysis
- **New Data**: Loaded into BigQuery tables as part of ETL process
- **Entity Resolution**: Can query historical data from BigQuery and write results back
- **AML Detection**: Run detection queries directly in BigQuery using SQL functions

## Folder Structure

```
bigquery/
├── config/          # BigQuery configuration (project, dataset, credentials)
├── schemas/         # JSON schema definitions for all tables
├── ddl/             # Data Definition Language - CREATE TABLE statements
├── dml/             # Data Manipulation Language - ETL, merges, updates
├── etl/             # ETL pipeline scripts (load, transform, validate)
└── README.md        # This file
```

## Prerequisites

1. Google Cloud Project with BigQuery API enabled
2. Service account with BigQuery Data Editor and Job User roles
3. Environment variables configured:
   - `GOOGLE_APPLICATION_CREDENTIALS` - Path to service account JSON
   - `BQ_PROJECT_ID` - GCP Project ID
   - `BQ_DATASET_ID` - BigQuery dataset name (e.g., fincrime_er)
   - `BQ_LOCATION` - Dataset location (e.g., US, EU)

## Setup Instructions

### 1. Create Dataset
```bash
bq mk --dataset --location=US your-project-id:fincrime_er
```

### 2. Create Tables
Run DDL scripts in order:
```bash
bq query --use_legacy_sql=false < ddl/01_create_raw_tables.sql
bq query --use_legacy_sql=false < ddl/02_create_staging_tables.sql
bq query --use_legacy_sql=false < ddl/03_create_resolved_tables.sql
bq query --use_legacy_sql=false < ddl/04_create_graph_tables.sql
bq query --use_legacy_sql=false < ddl/05_create_alerts_tables.sql
```

### 3. Configure ETL
Update `config/bq_config.json` with your project details

### 4. Load Data
```bash
python etl/load_historical_data.py
python etl/load_new_data.py
```

## Table Design

### Raw Layer
- `raw_customers` - Raw customer profile data
- `raw_transactions` - Raw transaction logs

### Staging Layer
- `stg_customers_standardized` - Standardized/cleaned customer data
- `stg_transactions_enriched` - Enriched transaction data

### Resolved Layer
- `resolved_customers` - Customers mapped to golden entities
- `golden_entities` - Consolidated golden entity records

### Graph Layer
- `entity_transaction_graph` - Customer-Transaction graph edges
- `entity_features` - Node features
- `entity_edge_features` - Edge features

### Alerts Layer
- `aml_alerts` - All AML/Fraud alerts
- `alert_investigations` - Investigation tracking

## Usage with Python Engine

```python
from src.bigquery.bq_client import BigQueryClient
from src.er.pipeline import EntityResolutionPipeline

bq = BigQueryClient()
# Load historical data from BigQuery
customers_df = bq.query_to_dataframe("SELECT * FROM fincrime_er.raw_customers WHERE load_date >= '2024-01-01'")
# Run ER pipeline
pipeline = EntityResolutionPipeline()
resolved, golden = pipeline.resolve(customers_df)
# Write results back to BigQuery
bq.dataframe_to_table(resolved, 'resolved_customers', if_exists='append')
```
