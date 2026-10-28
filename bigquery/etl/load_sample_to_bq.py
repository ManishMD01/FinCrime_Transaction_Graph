#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.bigquery.bq_client import BigQueryClient
import pandas as pd
from datetime import datetime, timedelta

bq = BigQueryClient()

# Sample customers
customers = pd.DataFrame({
    'customer_id': ['1','2','3','4','5','6'],
    'name': ['John Smith', 'Jon Smith', 'Jane Doe', 'Bob Johnson', 'Robert Johnson', 'Alice Brown'],
    'dob': ['1980-01-01','1980-01-01','1990-05-05','1975-03-15','1975-03-15','1985-07-20'],
    'address': ['123 Main St','123 Main Street','456 Oak Ave','789 Pine Rd','789 Pine Road','321 Elm St'],
    'phone': ['5551234567','5551234567','5559998888','5554443333','5554443333','5557776666'],
    'email': ['john@gmail.com','john@gmail.com','jane@yahoo.com','bob@gmail.com','robert@gmail.com','alice@gmail.com'],
    'ssn': ['123456789','123456789','987654321','555667777','555667777','111223333'],
    'zip': ['10001','10001','90210','77001','77001','33101'],
    'device_id': ['DEV001','DEV001','DEV002','DEV003','DEV003','DEV004'],
    'ip_address': ['1.1.1.1','1.1.1.1','2.2.2.2','3.3.3.3','3.3.3.3','4.4.4.4'],
    'location': ['NY','NY','CA','TX','TX','FL'],
    'source_system': ['SAMPLE']*6,
    'load_date': [datetime.now().date()]*6,
    'load_timestamp': [datetime.now()]*6,
    'batch_id': ['SAMPLE']*6
})
bq.dataframe_to_table(customers, 'raw_customers', if_exists='replace')

# Sample transactions with recent dates
now = datetime.now()
transactions = pd.DataFrame({
    'transaction_id': [f'T{i}' for i in range(1,11)],
    'sender_id': ['1','1','1','1','4','4','5','2','6','3'],
    'receiver_id': ['3','3','3','3','5','5','4','4','5','1'],
    'amount': [9500,9400,9600,9300,15000,14000,2000,2100,3000,4000],
    'currency': ['USD']*10,
    'timestamp': [now - timedelta(hours=i) for i in range(10)],
    'transaction_date': [(now - timedelta(hours=i)).date() for i in range(10)],
    'channel': ['wire']*10,
    'location': ['NY']*10,
    'transaction_type': ['transfer']*10,
    'beneficiary_account': ['']*10,
    'source_system': ['SAMPLE']*10,
    'load_date': [datetime.now().date()]*10,
    'load_timestamp': [datetime.now()]*10,
    'batch_id': ['SAMPLE']*10
})
bq.dataframe_to_table(transactions, 'raw_transactions', if_exists='replace')
print('Done')
