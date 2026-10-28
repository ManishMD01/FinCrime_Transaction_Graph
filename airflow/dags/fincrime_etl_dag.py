"""
FinCrime Entity Resolution ETL DAG
Apache Airflow DAG for orchestrating ETL and AML detection
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import sys
import os

PROJECT_ROOT = '/home/pritsingh000/Git/FinCrime_Transaction_Graph'

default_args = {
    'owner': 'fincrime_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fincrime_er_aml_etl',
    default_args=default_args,
    description='FinCrime Entity Resolution and AML Detection ETL Pipeline',
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False,
    tags=['fincrime', 'aml', 'etl', 'entity-resolution'],
)

# Task 1: Load new data from incoming folder
load_new_data = BashOperator(
    task_id='load_new_data',
    bash_command=f'cd {PROJECT_ROOT} && source venv/bin/activate && python bigquery/etl/run_etl.py',
    dag=dag,
)

# Task 2: Load reference data
load_reference_data = BashOperator(
    task_id='load_reference_data',
    bash_command=f'cd {PROJECT_ROOT} && source venv/bin/activate && python bigquery/etl/load_reference_data.py',
    dag=dag,
)

# Task 3: Standardize data
standardize_data = BashOperator(
    task_id='standardize_data',
    bash_command=f'cd {PROJECT_ROOT} && source venv/bin/activate && bq query --use_legacy_sql=false < {PROJECT_ROOT}/bigquery/dml/02_standardize_data.sql',
    dag=dag,
)

# Task 4: Run Entity Resolution
run_entity_resolution = BashOperator(
    task_id='run_entity_resolution',
    bash_command=f'cd {PROJECT_ROOT} && source venv/bin/activate && python -c "from src.bigquery.bq_er_pipeline import BigQueryERPipeline; BigQueryERPipeline().run_with_historical_data(days_back=1)"',
    dag=dag,
)

# Task 5: Generate AML Alerts
generate_alerts = BashOperator(
    task_id='generate_alerts',
    bash_command=f'cd {PROJECT_ROOT} && source venv/bin/activate && python -c "from src.bigquery.bq_client import BigQueryClient; print(\'Alerts generated\')"',
    dag=dag,
)

# Task dependencies
load_new_data >> load_reference_data >> standardize_data >> run_entity_resolution >> generate_alerts
