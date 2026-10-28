# ETL Process for Huge Data

## Files
- `etl_huge_data.py` - Chunked loading for large datasets (10K+ customers, 100K+ transactions)
- `load_with_validation.py` - File-based ETL with validation and duplicate prevention
- `run_etl.py` - Main orchestrator for file-based ETL
- `load_historical_data.py` - Load historical CSV data
- `load_new_data.py` - Incremental loading with MERGE
- `load_reference_data.py` - Load reference/lookup data

## Usage for Huge Data
```bash
cd /home/pritsingh000/Git/FinCrime_Transaction_Graph
source venv/bin/activate
unset GOOGLE_APPLICATION_CREDENTIALS
python bigquery/etl/etl_huge_data.py
```

## Features
- Chunked processing (10K rows per chunk)
- Progress tracking
- Batch ID tracking
- Partitioned table loading
