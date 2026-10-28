#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.bigquery.bq_client import BigQueryClient
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
from google.cloud import bigquery

c = BigQueryClient()
# Check schemas
for table in ['raw_customers', 'raw_transactions']:
    schema = c.client.get_table(f"{c.dataset_ref}.{table}").schema
    print(f"\n{table}:")
    for s in schema:
        print(f"  {s.name}: {s.field_type} {s.mode}")
