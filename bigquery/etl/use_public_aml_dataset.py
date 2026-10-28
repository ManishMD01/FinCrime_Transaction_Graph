#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.bigquery.bq_client import BigQueryClient
import pandas as pd
from datetime import datetime

bq = BigQueryClient()
# Create sample AML dataset structure
# Using common public dataset patterns

# Try to create customers from Bitcoin transactions or use mock AML data
query = """
SELECT DISTINCT from_address as address, COUNT(*) as tx_count
FROM `bigquery-public-data.crypto_bitcoin.transactions`
WHERE block_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY from_address
LIMIT 50
"""
try:
    df = bq.client.query(query).to_dataframe()
    customers = []
    for idx, row in df.iterrows():
        customers.append({
            'customer_id': str(idx+1),
            'name': f'Entity {idx+1}',
            'dob': '1980-01-01',
            'address': row['address'],
            'phone': f'555{idx:07d}',
            'email': f'entity{idx+1}@example.com',
            'ssn': f'{idx:09d}',
            'zip': '00000',
            'device_id': f'DEV{idx:04d}',
            'ip_address': f'10.0.{idx%255}.{idx%255}',
            'location': 'US',
            'source_system': 'PUBLIC_AML',
            'load_date': datetime.now().date(),
            'load_timestamp': datetime.now(),
            'batch_id': 'PUBLIC_AML'
        })
    df_cust = pd.DataFrame(customers)
    bq.dataframe_to_table(df_cust, 'raw_customers', if_exists='replace')
    print(f'Loaded {len(df_cust)} customers')
except Exception as e:
    print(e)
