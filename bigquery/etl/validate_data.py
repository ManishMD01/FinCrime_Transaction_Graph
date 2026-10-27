#!/usr/bin/env python3
"""
Data Validation Module for ETL
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from google.cloud import bigquery
import pandas as pd

class DataValidator:
    def __init__(self, config_path='bigquery/config/bq_config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        
        import os
        self.project_id = os.environ.get('BQ_PROJECT_ID', self.config['project_id'])
        self.dataset_id = self.config['dataset_id']
        self.client = bigquery.Client(project=self.project_id)
        self.dataset_ref = f"{self.project_id}.{self.dataset_id}"
    
    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def is_file_already_loaded(self, filepath):
        """Check if file was already loaded"""
        file_hash = self.calculate_file_hash(filepath)
        file_name = Path(filepath).name
        
        query = f"""
        SELECT COUNT(*) as cnt
        FROM `{self.dataset_ref}.etl_file_tracking`
        WHERE file_hash = '{file_hash}' AND status = 'LOADED'
        """
        try:
            result = self.client.query(query).to_dataframe()
            if result['cnt'].iloc[0] > 0:
                return True, "File already loaded (same hash)"
        except:
            pass
        
        query2 = f"""
        SELECT COUNT(*) as cnt
        FROM `{self.dataset_ref}.etl_file_tracking`
        WHERE file_name = '{file_name}' AND status = 'LOADED'
        """
        try:
            result = self.client.query(query2).to_dataframe()
            if result['cnt'].iloc[0] > 0:
                return True, "File with same name already loaded"
        except:
            pass
        
        return False, None
    
    def validate_customers(self, df):
        """Validate customer data"""
        errors = []
        required = ['customer_id', 'name']
        for col in required:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")
        
        if df['customer_id'].isnull().sum() > 0:
            errors.append(f"{df['customer_id'].isnull().sum()} null customer_ids")
        
        if df['customer_id'].duplicated().sum() > 0:
            errors.append(f"{df['customer_id'].duplicated().sum()} duplicate customer_ids in file")
        
        return len(errors) == 0, errors
    
    def validate_transactions(self, df):
        """Validate transaction data"""
        errors = []
        required = ['transaction_id', 'sender_id', 'receiver_id', 'amount', 'timestamp']
        for col in required:
            if col not in df.columns:
                errors.append(f"Missing required column: {col}")
        
        if df['transaction_id'].isnull().sum() > 0:
            errors.append(f"{df['transaction_id'].isnull().sum()} null transaction_ids")
        
        if (df['amount'] <= 0).sum() > 0:
            errors.append(f"{(df['amount'] <= 0).sum()} transactions with amount <= 0")
        
        if df['transaction_id'].duplicated().sum() > 0:
            errors.append(f"{df['transaction_id'].duplicated().sum()} duplicate transaction_ids in file")
        
        return len(errors) == 0, errors
    
    def track_file(self, filepath, file_type, batch_id, status='PENDING'):
        """Track file in ETL tracking table"""
        file_hash = self.calculate_file_hash(filepath)
        file_name = Path(filepath).name
        file_size = Path(filepath).stat().st_size
        
        df = pd.read_csv(filepath)
        rows_count = len(df)
        
        track_df = pd.DataFrame([{
            'file_id': hashlib.md5(f"{file_name}_{file_hash}".encode()).hexdigest(),
            'file_name': file_name,
            'file_path': str(filepath),
            'file_type': file_type,
            'file_hash': file_hash,
            'file_size_bytes': file_size,
            'rows_count': rows_count,
            'status': status,
            'batch_id': batch_id,
            'source_system': 'FILE_UPLOAD',
            'loaded_to_table': '',
            'loaded_rows': 0,
            'duplicate_rows': 0,
            'rejected_rows': 0,
            'load_date': datetime.now().date(),
            'load_timestamp': datetime.now(),
            'processed_timestamp': None,
            'error_message': '',
            'checksum_verified': True
        }])
        
        table_id = f"{self.dataset_ref}.etl_file_tracking"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
        try:
            job = self.client.load_table_from_dataframe(track_df, table_id, job_config=job_config)
            job.result()
        except Exception as e:
            print(f"Warning: Could not track file: {e}")
        
        return track_df['file_id'].iloc[0]

if __name__ == '__main__':
    validator = DataValidator()
    print("Data validator ready")
