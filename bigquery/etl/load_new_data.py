#!/usr/bin/env python3
"""
Load New Data into BigQuery as part of ETL Process
"""

import os
import json
import uuid
from datetime import datetime
from google.cloud import bigquery
import pandas as pd

class NewDataLoader:
    def __init__(self, config_path='bigquery/config/bq_config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.project_id = os.environ.get('BQ_PROJECT_ID', self.config['project_id'])
        self.dataset_id = self.config['dataset_id']
        self.client = bigquery.Client(project=self.project_id)
        self.dataset_ref = f"{self.project_id}.{self.dataset_id}"
        self.batch_id = f"NEW_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    
    def load_new_customers(self, df, source_system='ETL_STREAM'):
        """Load new customers to staging then to raw"""
        staging_df = df.copy()
        staging_df['source_system'] = source_system
        staging_df['load_date'] = datetime.now().date()
        staging_df['load_timestamp'] = datetime.now()
        staging_df['batch_id'] = self.batch_id
        staging_df['load_processed'] = False
        
        # Load to staging first
        staging_table = f"{self.dataset_ref}.staging_new_customers"
        job = self.client.load_table_from_dataframe(staging_df, staging_table)
        job.result()
        print(f"Loaded {len(staging_df)} new customers to staging")
        
        # Run merge to raw
        query = """
        MERGE `""" + self.dataset_ref + """.raw_customers` T
        USING (
          SELECT * FROM `""" + self.dataset_ref + """.staging_new_customers`
          WHERE batch_id = '""" + self.batch_id + """' AND load_processed = FALSE
        ) S
        ON T.customer_id = S.customer_id AND T.source_system = S.source_system
        WHEN NOT MATCHED THEN
          INSERT (customer_id, name, dob, address, phone, email, ssn, zip, device_id, ip_address, location, source_system, load_date, load_timestamp, batch_id)
          VALUES (S.customer_id, S.name, S.dob, S.address, S.phone, S.email, S.ssn, S.zip, S.device_id, S.ip_address, S.location, S.source_system, S.load_date, S.load_timestamp, S.batch_id)
        """
        job = self.client.query(query)
        job.result()
        
        # Mark processed
        self.client.query(f"UPDATE `{self.dataset_ref}.staging_new_customers` SET load_processed = TRUE WHERE batch_id = '{self.batch_id}'").result()
        print("New customers merged to raw_customers")
    
    def load_new_transactions(self, df, source_system='ETL_STREAM'):
        """Load new transactions to staging then to raw"""
        staging_df = df.copy()
        staging_df['timestamp'] = pd.to_datetime(staging_df['timestamp'])
        staging_df['transaction_date'] = staging_df['timestamp'].dt.date
        staging_df['currency'] = staging_df.get('currency', 'USD')
        staging_df['beneficiary_account'] = staging_df.get('beneficiary_account', None)
        staging_df['source_system'] = source_system
        staging_df['load_date'] = datetime.now().date()
        staging_df['load_timestamp'] = datetime.now()
        staging_df['batch_id'] = self.batch_id
        staging_df['load_processed'] = False
        
        staging_table = f"{self.dataset_ref}.staging_new_transactions"
        job = self.client.load_table_from_dataframe(staging_df, staging_table)
        job.result()
        print(f"Loaded {len(staging_df)} new transactions to staging")
        
        # Merge to raw
        query = f"""
        MERGE `{self.dataset_ref}.raw_transactions` T
        USING (
          SELECT * FROM `{self.dataset_ref}.staging_new_transactions`
          WHERE batch_id = '{self.batch_id}' AND load_processed = FALSE
        ) S
        ON T.transaction_id = S.transaction_id
        WHEN NOT MATCHED THEN
          INSERT (transaction_id, sender_id, receiver_id, amount, currency, timestamp, transaction_date, channel, location, transaction_type, beneficiary_account, source_system, load_date, load_timestamp, batch_id)
          VALUES (S.transaction_id, S.sender_id, S.receiver_id, S.amount, S.currency, S.timestamp, S.transaction_date, S.channel, S.location, S.transaction_type, S.beneficiary_account, S.source_system, S.load_date, S.load_timestamp, S.batch_id)
        """
        job = self.client.query(query)
        job.result()
        
        self.client.query(f"UPDATE `{self.dataset_ref}.staging_new_transactions` SET load_processed = TRUE WHERE batch_id = '{self.batch_id}'").result()
        print("New transactions merged to raw_transactions")

if __name__ == '__main__':
    loader = NewDataLoader()
    print("New data loader ready for ETL integration")
