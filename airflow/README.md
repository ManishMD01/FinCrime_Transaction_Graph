# Apache Airflow DAG for FinCrime ETL

## Setup

1. Install Airflow (optional):
```bash
pip install apache-airflow
```

2. Copy DAG to Airflow dags folder:
```bash
cp airflow/dags/fincrime_etl_dag.py $AIRFLOW_HOME/dags/
```

3. Start Airflow:
```bash
airflow webserver -p 8080
airflow scheduler
```

4. Access Airflow UI at http://localhost:8080

## DAG: fincrime_er_aml_etl

This DAG runs daily and:
1. Loads new data from `data/incoming/` 
2. Loads reference data
3. Standardizes data
4. Runs Entity Resolution
5. Generates AML alerts

## Manual Trigger
From Airflow UI, enable and trigger the DAG manually.
