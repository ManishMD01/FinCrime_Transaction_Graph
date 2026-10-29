"""
FinCrime Huge Data ETL DAG - For large dataset processing
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
import os

PROJECT_ROOT = os.environ.get('PROJECT_ROOT', '/home/pritsingh000/Git/FinCrime_Transaction_Graph')
VENV_ACTIVATE = f'source {PROJECT_ROOT}/venv/bin/activate'

default_args = {
    'owner': 'fincrime_data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
    'execution_timeout': timedelta(hours=4),
}

dag = DAG(
    'fincrime_huge_data_etl',
    default_args=default_args,
    description='ETL Pipeline for Huge Datasets with Chunked Processing',
    schedule_interval=None,  # Manual trigger only for large jobs
    catchup=False,
    tags=['fincrime', 'etl', 'bigdata', 'huge-data'],
)

# Load huge dataset in chunks
load_huge_data = BashOperator(
    task_id='load_huge_dataset_chunked',
    bash_command=f'cd {PROJECT_ROOT} && {VENV_ACTIVATE} && GOOGLE_APPLICATION_CREDENTIALS="" PYTHONPATH={PROJECT_ROOT}:{PROJECT_ROOT}/src:{PROJECT_ROOT}/bigquery python bigquery/etl/etl_huge_data.py',
    dag=dag,
)

# Process huge data through pipeline
process_huge_data = BashOperator(
    task_id='process_huge_data_pipeline',
    bash_command=f'cd {PROJECT_ROOT} && {VENV_ACTIVATE} && GOOGLE_APPLICATION_CREDENTIALS="" PYTHONPATH={PROJECT_ROOT}:{PROJECT_ROOT}/src:{PROJECT_ROOT}/bigquery python -c "from src.bigquery.bq_er_pipeline import BigQueryERPipeline; BigQueryERPipeline().run_with_historical_data(days_back=3650)"',
    dag=dag,
)

load_huge_data >> process_huge_data
