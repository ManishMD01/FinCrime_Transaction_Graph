#!/usr/bin/env python3
import sys
import json
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph')
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph/src')
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph/bigquery')

from src.bigquery.bq_client import BigQueryClient

search_type = sys.argv[1] if len(sys.argv) > 1 else ''
search_term = sys.argv[2] if len(sys.argv) > 2 else ''

try:
    c = BigQueryClient()
    result = {}
    if search_type == 'customer_id':
        df = c.query_to_dataframe(f"SELECT * FROM `{c.dataset_ref}.raw_customers` WHERE customer_id = '{search_term}'")
        result['customers'] = df.to_dict('records')
        txns = c.query_to_dataframe(f"SELECT * FROM `{c.dataset_ref}.raw_transactions` WHERE CAST(sender_id AS STRING) = '{search_term}' OR CAST(receiver_id AS STRING) = '{search_term}' ORDER BY timestamp DESC")
        result['transactions'] = txns.to_dict('records')
    elif search_type == 'transaction_id':
        df = c.query_to_dataframe(f"SELECT * FROM `{c.dataset_ref}.raw_transactions` WHERE transaction_id = '{search_term}'")
        result['transactions'] = df.to_dict('records')
    elif search_type == 'golden_entity_id':
        res = c.query_to_dataframe(f"SELECT * FROM `{c.dataset_ref}.resolved_customers` WHERE CAST(golden_entity_id AS STRING) = '{search_term}'")
        result['resolved'] = res.to_dict('records')
    else:
        result = {'info': 'Search completed'}
    print(json.dumps(result, default=str))
except Exception as e:
    print(json.dumps({'error': str(e)}))
