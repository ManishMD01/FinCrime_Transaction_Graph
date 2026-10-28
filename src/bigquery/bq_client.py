"""
BigQuery Client for FinCrime Engine
"""

import os
import sys
from pathlib import Path
from google.cloud import bigquery
import pandas as pd

# Add parent dirs to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from bigquery.config.config import config
except:
    try:
        from src.bigquery.config import config
    except:
        class DummyConfig:
            project_id = os.environ.get('GCP_PROJECT_ID', 'nalen-458109')
            dataset_id = os.environ.get('BQ_DATASET_ID', 'fincrime_er')
            location = os.environ.get('BQ_LOCATION', 'US')
        config = DummyConfig()


class BigQueryClient:
    """BigQuery client for FinCrime Entity Resolution Engine"""
    
    def __init__(self, config_path=None):
        self.config_obj = config
        self.project_id = getattr(self.config_obj, 'project_id', os.environ.get('GCP_PROJECT_ID'))
        self.dataset_id = getattr(self.config_obj, 'dataset_id', os.environ.get('BQ_DATASET_ID', 'fincrime_er'))
        self.location = getattr(self.config_obj, 'location', os.environ.get('BQ_LOCATION', 'US'))
        self.client = bigquery.Client(project=self.project_id, location=self.location)
        self.dataset_ref = f"{self.project_id}.{self.dataset_id}"
        self.config = {'project_id': self.project_id, 'dataset_id': self.dataset_id, 'location': self.location}
    
    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        query_job = self.client.query(query)
        return query_job.to_dataframe()
    
    def dataframe_to_table(self, df: pd.DataFrame, table_name: str, if_exists: str = 'append') -> None:
        table_id = f"{self.dataset_ref}.{table_name}"
        if if_exists == 'replace':
            write_disposition = "WRITE_TRUNCATE"
        elif if_exists == 'append':
            write_disposition = "WRITE_APPEND"
        else:
            write_disposition = "WRITE_EMPTY"
        job_config = bigquery.LoadJobConfig(write_disposition=write_disposition)
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Loaded {len(df)} rows to {table_id}")
    
    def get_historical_customers(self, days_back: int = 365) -> pd.DataFrame:
        if days_back >= 36500:
            query = f"SELECT * FROM `{self.dataset_ref}.raw_customers` ORDER BY load_date DESC"
        else:
            query = f"SELECT * FROM `{self.dataset_ref}.raw_customers` WHERE load_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY) ORDER BY load_date DESC"
        return self.query_to_dataframe(query)
    
    def get_historical_transactions(self, days_back: int = 365) -> pd.DataFrame:
        if days_back >= 36500:
            query = f"SELECT * FROM `{self.dataset_ref}.raw_transactions` ORDER BY timestamp DESC"
        else:
            query = f"SELECT * FROM `{self.dataset_ref}.raw_transactions` WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY) ORDER BY timestamp DESC"
        return self.query_to_dataframe(query)
    
    def get_new_customers_since(self, since_date: str) -> pd.DataFrame:
        query = f"SELECT * FROM `{self.dataset_ref}.raw_customers` WHERE load_date >= '{since_date}' ORDER BY load_timestamp DESC"
        return self.query_to_dataframe(query)
    
    def get_new_transactions_since(self, since_date: str) -> pd.DataFrame:
        query = f"SELECT * FROM `{self.dataset_ref}.raw_transactions` WHERE load_date >= '{since_date}' ORDER BY load_timestamp DESC"
        return self.query_to_dataframe(query)
    
    def run_aml_detection_queries(self) -> pd.DataFrame:
        query = f"SELECT * FROM `{self.dataset_ref}.vw_alert_summary` ORDER BY alert_date DESC, alert_count DESC"
        return self.query_to_dataframe(query)
