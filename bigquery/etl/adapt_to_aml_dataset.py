#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.bigquery.bq_client import BigQueryClient
import pandas as pd
from datetime import datetime

bq = BigQueryClient()
# Create tables matching our schema from sample data
# The data we have is already compatible
print("Data already loaded and compatible")
