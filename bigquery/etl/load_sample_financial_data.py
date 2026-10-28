#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.bigquery.bq_client import BigQueryClient
import pandas as pd
from datetime import datetime, timedelta
import random

bq = BigQueryClient()

# Create sample financial AML dataset
customers = []
names = ['John Smith', 'Maria Garcia', 'Ahmed Hassan', 'Li Wei', 'James Wilson', 'Sarah Johnson']
for i in range(1, 31):
    customers.append({
        'customer_id': str(i),
        'name': random.choice(names) + f' {i}',
        'dob': f'{1970+i%30}-0{i%9+1}-15',
        'address': f'{random.randint(100,999)} {random.choice(["Main","Oak","Pine"])} St',
        'phone': f'+1-555-{random.randint(1000000,9999999)}',
        'email': f'customer{i}@email.com',
        'ssn': f'{random.randint(100000000,999999999)}',
        'zip': f'{random.randint(10000,99999)}',
        'device_id': f'DEV{random.randint(1000,9999)}',
        'ip_address': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
        'location': random.choice(['US', 'UK', 'CA', 'MX']),
        'source_system': 'FIN_SAMPLE',
        'load_date': datetime.now().date(),
        'load_timestamp': datetime.now(),
        'batch_id': 'FIN_SAMPLE'
    })
df_cust = pd.DataFrame(customers)
bq.dataframe_to_table(df_cust, 'raw_customers', if_exists='replace')
print(f'Loaded {len(df_cust)} customers')

# Generate transactions with some suspicious patterns
transactions = []
now = datetime.now()
txn_id = 1
# Normal transactions
for i in range(100):
    sender = str(random.randint(1, 30))
    receiver = str(random.randint(1, 30))
    if sender == receiver: continue
    transactions.append({
        'transaction_id': f'FTXN{txn_id:06d}',
        'sender_id': sender,
        'receiver_id': receiver,
        'amount': round(random.uniform(50, 5000), 2),
        'currency': 'USD',
        'timestamp': now - timedelta(days=random.randint(0, 30)),
        'transaction_date': (now - timedelta(days=random.randint(0, 30))).date(),
        'channel': random.choice(['ACH', 'WIRE', 'ONLINE']),
        'location': random.choice(['US', 'UK', 'CA']),
        'transaction_type': 'TRANSFER',
        'beneficiary_account': f'ACC{random.randint(10000,99999)}',
        'source_system': 'FIN_SAMPLE',
        'load_date': datetime.now().date(),
        'load_timestamp': datetime.now(),
        'batch_id': 'FIN_SAMPLE'
    })
    txn_id += 1

# Add structuring pattern
for i in range(5):
    transactions.append({
        'transaction_id': f'FTXN{txn_id:06d}',
        'sender_id': '1',
        'receiver_id': '15',
        'amount': round(random.uniform(9000, 9900), 2),
        'currency': 'USD',
        'timestamp': now - timedelta(hours=i*2),
        'transaction_date': now.date(),
        'channel': 'WIRE',
        'location': 'US',
        'transaction_type': 'TRANSFER',
        'beneficiary_account': 'ACC99999',
        'source_system': 'FIN_SAMPLE',
        'load_date': datetime.now().date(),
        'load_timestamp': datetime.now(),
        'batch_id': 'FIN_SAMPLE'
    })
    txn_id += 1

df_txn = pd.DataFrame(transactions)
bq.dataframe_to_table(df_txn, 'raw_transactions', if_exists='replace')
print(f'Loaded {len(df_txn)} transactions')
