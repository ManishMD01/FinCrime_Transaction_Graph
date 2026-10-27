#!/usr/bin/env python3
"""
Load Historical Data into BigQuery
"""

import os
import json
from datetime import datetime
from google.cloud import bigquery
import pandas as pd

class HistoricalDataLoader:
    def __init__(self, config_path='bigquery/config/bq_config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.project_id = os.environ.get('BQ_PROJECT_ID', self.config['project_id'])
        self.dataset_id = self.config['dataset_id']
        self.client = bigquery.Client(project=self.project_id)
        self.dataset_ref = f"{self.project_id}.{self.dataset_id}"
    
    def load_customers_from_csv(self, csv_path, source_system='HISTORICAL'):
        """Load historical customers from CSV"""
        df = pd.read_csv(csv_path)
        df['source_system'] = source_system
        df['load_date'] = datetime.now().date()
        df['load_timestamp'] = datetime.now()
        df['batch_id'] = f"HIST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        table_id = f"{self.dataset_ref}.raw_customers"
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            schema=[
                bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("dob", "DATE"),
                bigquery.SchemaField("address", "STRING"),
                bigquery.SchemaField("phone", "STRING"),
                bigquery.SchemaField("email", "STRING"),
                bigquery.SchemaField("ssn", "STRING"),
                bigquery.SchemaField("zip", "STRING"),
                bigquery.SchemaField("device_id", "STRING"),
                bigquery.SchemaField("ip_address", "STRING"),
                bigquery.SchemaField("location", "STRING"),
                bigquery.SchemaField("source_system", "STRING"),
                bigquery.SchemaField("load_date", "DATE", mode="REQUIRED"),
                bigquery.SchemaField("load_timestamp", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("batch_id", "STRING"),
            ],
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="load_date"
            )
        )
        
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Loaded {len(df)} customer records to {table_id}")
    
    def load_transactions_from_csv(self, csv_path, source_system='HISTORICAL'):
        """Load historical transactions from CSV"""
        df = pd.read_csv(csv_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['transaction_date'] = df['timestamp'].dt.date
        df['currency'] = df.get('currency', 'USD')
        df['beneficiary_account'] = df.get('beneficiary_account', None)
        df['source_system'] = source_system
        df['load_date'] = datetime.now().date()
        df['load_timestamp'] = datetime.now()
        df['batch_id'] = f"HIST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        table_id = f"{self.dataset_ref}.raw_transactions"
        job = self.client.load_table_from_dataframe(df, table_id)
        job.result()
        print(f"Loaded {len(df)} transaction records to {table_id}")

if __name__ == '__main__':
    loader = HistoricalDataLoader()
    # Example usage:
    # loader.load_customers_from_csv('data/historical_customers.csv')
    # loader.load_transactions_from_csv('data/historical_transactions.csv')
    print("Historical data loader ready. Update paths and uncomment to load.")
