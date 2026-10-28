#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.bigquery.bq_client import BigQueryClient
import pandas as pd
from datetime import datetime, timedelta
import random

bq = BigQueryClient()

# Generate 50 customers
customers = []
for i in range(1, 51):
    customers.append({
        'customer_id': str(i),
        'name': f'Customer {i} Smith' if i % 3 == 0 else f'User {i} Doe',
        'dob': f'198{i%10}-01-0{i%9+1}',
        'address': f'{i*100} Main St',
        'phone': f'555{1000000+i}',
        'email': f'user{i}@example.com',
        'ssn': f'{i:09d}',
        'zip': f'{10000+i%900}',
        'device_id': f'DEV{i%10:03d}',
        'ip_address': f'192.168.{i%255}.{i%255}',
        'location': random.choice(['NY', 'CA', 'TX', 'FL', 'WA']),
        'source_system': 'GEN',
        'load_date': datetime.now().date(),
        'load_timestamp': datetime.now(),
        'batch_id': 'GEN'
    })
df_cust = pd.DataFrame(customers)
bq.dataframe_to_table(df_cust, 'raw_customers', if_exists='replace')
print(f'Loaded {len(df_cust)} customers')

# Generate 200 transactions
transactions = []
now = datetime.now()
for i in range(1, 201):
    sender = str(random.randint(1, 50))
    receiver = str(random.randint(1, 50))
    if sender == receiver:
        continue
    transactions.append({
        'transaction_id': f'TXN{i:06d}',
        'sender_id': sender,
        'receiver_id': receiver,
        'amount': round(random.uniform(100, 15000), 2),
        'currency': 'USD',
        'timestamp': now - timedelta(hours=random.randint(0, 720)),
        'transaction_date': (now - timedelta(hours=random.randint(0, 720))).date(),
        'channel': random.choice(['wire', 'ach', 'online', 'mobile']),
        'location': random.choice(['NY', 'CA', 'TX', 'FL', 'WA']),
        'transaction_type': 'transfer',
        'beneficiary_account': '',
        'source_system': 'GEN',
        'load_date': datetime.now().date(),
        'load_timestamp': datetime.now(),
        'batch_id': 'GEN'
    })
df_txn = pd.DataFrame(transactions)
bq.dataframe_to_table(df_txn, 'raw_transactions', if_exists='replace')
print(f'Loaded {len(df_txn)} transactions')
