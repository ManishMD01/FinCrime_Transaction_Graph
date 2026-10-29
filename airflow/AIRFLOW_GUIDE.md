# Apache Airflow Guide for FinCrime ETL

## Available DAGs

### 1. fincrime_complete_etl_pipeline
- **Schedule**: Daily at 1 AM
- **Purpose**: Complete ETL pipeline for normal operations
- **Tasks**:
  1. Check incoming files
  2. Load and validate new data
  3. Load reference data
  4. Standardize data
  5. Entity Resolution
  6. Build graph features
  7. Generate AML alerts
  8. Data quality check

### 2. fincrime_huge_data_etl
- **Schedule**: Manual trigger only
- **Purpose**: Process large datasets with chunked loading
- **Tasks**:
  1. Load huge dataset in chunks
  2. Process through full pipeline

## Starting Airflow

```bash
cd /home/pritsingh000/Git/FinCrime_Transaction_Graph
export AIRFLOW_HOME=/home/pritsingh000/Git/FinCrime_Transaction_Graph/airflow
source venv/bin/activate

# Initialize (first time)
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Start webserver and scheduler
airflow webserver -p 8080 &
airflow scheduler &
```

## Access GUI
Open http://localhost:8080 (default login: admin/admin)

## Trigger DAG
From GUI or CLI:
```bash
airflow dags trigger fincrime_complete_etl_pipeline
```

## DAG Location
DAGs are in `airflow/dags/` and copied to AIRFLOW_HOME during setup.
