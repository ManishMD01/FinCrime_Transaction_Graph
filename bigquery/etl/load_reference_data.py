#!/usr/bin/env python3
"""
Load Reference Data into BigQuery
"""

import os
import json
from pathlib import Path
from datetime import datetime
from google.cloud import bigquery
import pandas as pd

class ReferenceDataLoader:
    def __init__(self, config_path='bigquery/config/bq_config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.project_id = os.environ.get('BQ_PROJECT_ID', self.config['project_id'])
        self.dataset_id = self.config['dataset_id']
        self.client = bigquery.Client(project=self.project_id)
        self.dataset_ref = f"{self.project_id}.{self.dataset_id}"
        self.ref_dir = Path('bigquery/reference_data')
    
    def load_csv_reference(self, filename, table_name):
        """Load CSV reference data"""
        filepath = self.ref_dir / filename
        if not filepath.exists():
            print(f"File not found: {filepath}")
            return
        
        df = pd.read_csv(filepath)
        df['load_date'] = datetime.now().date()
        
        table_id = f"{self.dataset_ref}.{table_name}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"Loaded {len(df)} records to {table_id}")
    
    def load_all_reference_data(self):
        """Load all reference data files"""
        print("Loading reference data...")
        self.load_csv_reference('country_codes.csv', 'ref_country_codes')
        self.load_csv_reference('currency_codes.csv', 'ref_currency_codes')
        self.load_csv_reference('channel_types.csv', 'ref_channel_types')
        self.load_csv_reference('transaction_types.csv', 'ref_transaction_types')
        self.load_csv_reference('sanctions_list_sample.csv', 'ref_sanctions_list')
        print("Reference data loaded successfully")

if __name__ == '__main__':
    loader = ReferenceDataLoader()
    loader.load_all_reference_data()
