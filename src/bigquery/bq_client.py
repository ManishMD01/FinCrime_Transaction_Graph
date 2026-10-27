"""
BigQuery Client for FinCrime Engine
"""

import os
import json
from typing import Optional
from google.cloud import bigquery
import pandas as pd


class BigQueryClient:
    """BigQuery client for FinCrime Entity Resolution Engine"""
    
    def __init__(self, config_path='bigquery/config/bq_config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.project_id = os.environ.get('BQ_PROJECT_ID', self.config['project_id'])
        self.dataset_id = self.config['dataset_id']
        self.location = self.config['location']
        self.client = bigquery.Client(project=self.project_id, location=self.location)
        self.dataset_ref = f"{self.project_id}.{self.dataset_id}"
    
    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        """Execute query and return results as DataFrame"""
        query_job = self.client.query(query)
        return query_job.to_dataframe()
    
    def dataframe_to_table(self, df: pd.DataFrame, table_name: str, 
                          if_exists: str = 'append') -> None:
        """Load DataFrame to BigQuery table"""
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
        """Fetch historical customer data"""
        query = f"""
        SELECT * FROM `{self.dataset_ref}.raw_customers`
        WHERE load_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
        ORDER BY load_date DESC
        """
        return self.query_to_dataframe(query)
    
    def get_historical_transactions(self, days_back: int = 365) -> pd.DataFrame:
        """Fetch historical transaction data"""
        query = f"""
        SELECT * FROM `{self.dataset_ref}.raw_transactions`
        WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL {days_back} DAY)
        ORDER BY timestamp DESC
        """
        return self.query_to_dataframe(query)
    
    def get_new_customers_since(self, since_date: str) -> pd.DataFrame:
        """Fetch new customers loaded since date"""
        query = f"""
        SELECT * FROM `{self.dataset_ref}.raw_customers`
        WHERE load_date >= '{since_date}'
        ORDER BY load_timestamp DESC
        """
        return self.query_to_dataframe(query)
    
    def get_new_transactions_since(self, since_date: str) -> pd.DataFrame:
        """Fetch new transactions loaded since date"""
        query = f"""
        SELECT * FROM `{self.dataset_ref}.raw_transactions`
        WHERE load_date >= '{since_date}'
        ORDER BY load_timestamp DESC
        """
        return self.query_to_dataframe(query)
    
    def run_aml_detection_queries(self) -> pd.DataFrame:
        """Run AML detection using BigQuery SQL views"""
        query = f"""
        SELECT * FROM `{self.dataset_ref}.vw_alert_summary`
        ORDER BY alert_date DESC, alert_count DESC
        """
        return self.query_to_dataframe(query)
