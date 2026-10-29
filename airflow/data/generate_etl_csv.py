#!/usr/bin/env python3
import pandas as pd
import random
from datetime import datetime, timedelta
import os

os.makedirs('/home/pritsingh000/Git/FinCrime_Transaction_Graph/data/airflow_input', exist_ok=True)
os.makedirs('/home/pritsingh000/Git/FinCrime_Transaction_Graph/data/incoming', exist_ok=True)

# Generate Customers CSV
customers = []
for i in range(1, 101):
    customers.append({
        'customer_id': f'C{i:05d}',
        'name': f'Customer {i}',
        'dob': f'{1965+i%40}-{(i%12)+1:02d}-{(i%28)+1:02d}',
        'address': f'{i*10} {random.choice(["Main","Oak","Elm","Pine"])} Street',
        'phone': f'555-{random.randint(100,999)}-{random.randint(1000,9999)}',
        'email': f'customer{i}@aml.org',
        'ssn': f'{random.randint(100000000,999999999)}',
        'zip': f'{random.randint(10000,99999)}',
        'device_id': f'DEV{random.randint(1000,9999)}',
        'ip_address': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
        'location': random.choice(['US', 'UK', 'CA', 'SG', 'HK'])
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv('/home/pritsingh000/Git/FinCrime_Transaction_Graph/data/airflow_input/customers.csv', index=False)
df_customers.to_csv('/home/pritsingh000/Git/FinCrime_Transaction_Graph/data/incoming/customers.csv', index=False)
print(f'Generated {len(df_customers)} customers')

# Generate Transactions CSV
transactions = []
now = datetime.now()
for i in range(1, 501):
    sender = f'C{random.randint(1,100):05d}'
    receiver = f'C{random.randint(1,100):05d}'
    if sender == receiver:
        continue
    transactions.append({
        'transaction_id': f'TXN{i:06d}',
        'sender_id': sender,
        'receiver_id': receiver,
        'amount': round(random.uniform(10, 20000), 2),
        'timestamp': (now - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S'),
        'channel': random.choice(['WIRE', 'ACH', 'ONLINE', 'MOBILE', 'SWIFT']),
        'location': random.choice(['US', 'UK', 'CA', 'SG', 'HK']),
        'transaction_type': random.choice(['TRANSFER', 'PAYMENT', 'WIRE_OUT'])
    })

df_transactions = pd.DataFrame(transactions)
df_transactions.to_csv('/home/pritsingh000/Git/FinCrime_Transaction_Graph/data/airflow_input/transactions.csv', index=False)
df_transactions.to_csv('/home/pritsingh000/Git/FinCrime_Transaction_Graph/data/incoming/transactions.csv', index=False)
print(f'Generated {len(df_transactions)} transactions')
