#!/usr/bin/env python3
"""
ETL Process for Large/Huge Dataset Loading
Handles chunked loading for large datasets into BigQuery
"""

import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
from google.cloud import bigquery

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from bigquery.config.config import config

class HugeDataETL:
    def __init__(self):
        self.config = config
        self.client = bigquery.Client(project=self.config.project_id, location=self.config.location)
        self.dataset_ref = self.config.get_dataset_ref()
        self.batch_id = f"HUGE_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        self.chunk_size = 10000
    
    def generate_huge_dataset(self, num_customers=100000, num_transactions=1000000):
        """Generate large synthetic dataset for ETL testing"""
        print(f"Generating {num_customers} customers and {num_transactions} transactions...")
        
        # Generate customers in chunks
        customers_data = []
        for i in range(1, num_customers + 1):
            customers_data.append({
                'customer_id': f'CUST{i:08d}',
                'name': f'Customer {i}',
                'dob': f'{1960 + i%50}-01-01',
                'address': f'{i%1000} Street {i%100}',
                'phone': f'555{str(i).zfill(7)}',
                'email': f'cust{i}@example.com',
                'ssn': f'{i%1000000000:09d}',
                'zip': f'{str(i%99999).zfill(5)}',
                'device_id': f'DEV{i%5000:05d}',
                'ip_address': f'{i%255}.{(i//255)%255}.{(i//65025)%255}.{i%255}',
                'location': ['US','UK','CA','MX','FR'][i%5],
                'source_system': 'HUGE_ETL',
                'load_date': datetime.now().date(),
                'load_timestamp': datetime.now(),
                'batch_id': self.batch_id
            })
            if len(customers_data) >= self.chunk_size:
                df = pd.DataFrame(customers_data)
                self._load_chunk(df, 'raw_customers')
                customers_data = []
        if customers_data:
            df = pd.DataFrame(customers_data)
            self._load_chunk(df, 'raw_customers')
        
        # Generate transactions
        transactions_data = []
        now = datetime.now()
        for i in range(1, num_transactions + 1):
            transactions_data.append({
                'transaction_id': f'TXN{i:010d}',
                'sender_id': f'CUST{np.random.randint(1, num_customers+1):08d}',
                'receiver_id': f'CUST{np.random.randint(1, num_customers+1):08d}',
                'amount': round(np.random.exponential(5000), 2),
                'currency': 'USD',
                'timestamp': now - timedelta(hours=np.random.randint(0, 8760)),
                'transaction_date': (now - timedelta(hours=np.random.randint(0, 8760))).date(),
                'channel': np.random.choice(['WIRE','ACH','ONLINE','MOBILE']),
                'location': np.random.choice(['US','UK','CA','MX','FR']),
                'transaction_type': 'TRANSFER',
                'beneficiary_account': f'ACC{i%100000:06d}',
                'source_system': 'HUGE_ETL',
                'load_date': datetime.now().date(),
                'load_timestamp': datetime.now(),
                'batch_id': self.batch_id
            })
            if len(transactions_data) >= self.chunk_size:
                df = pd.DataFrame(transactions_data)
                self._load_chunk(df, 'raw_transactions')
                transactions_data = []
                if i % 100000 == 0:
                    print(f"  Loaded {i} transactions...")
        if transactions_data:
            df = pd.DataFrame(transactions_data)
            self._load_chunk(df, 'raw_transactions')
        
        print("Huge dataset generation complete!")
    
    def _load_chunk(self, df, table_name):
        table_id = f"{self.dataset_ref}.{table_name}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()

if __name__ == '__main__':
    etl = HugeDataETL()
    etl.generate_huge_dataset(num_customers=10000, num_transactions=100000)
