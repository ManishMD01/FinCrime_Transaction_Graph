# FinCrime Entity Resolution (ER) & Transaction Graph Engine

A high-performance, production-grade Entity Resolution (ER) engine designed for Financial Crime Compliance, Anti-Money Laundering (AML), and Fraud Detection. The engine connects disjointed customer profiles and flags suspicious transactional patterns by building unified golden entities from fragmented data.

## Overview

This system ingests fragmented customer profiles and transaction logs to:
1. **Resolve entities** - Link seemingly unrelated customer records that belong to the same individual/organization
2. **Build a unified transaction graph** - Connect all transactions to resolved golden entities
3. **Detect suspicious patterns** - Identify structuring/smurfing, money mule networks, and rapid velocity/phantom profiles

## Architecture

### Phase 1: Entity Resolution Pipeline
1. **Data Standardization** - Clean and normalize names, addresses, phones, emails, IDs
2. **Blocking/Indexing** - Reduce O(N²) to efficient candidate pairs using phonetic keys, zip codes, LSH
3. **Record Linkage** - Deterministic rules + probabilistic fuzzy matching (Jaro-Winkler, Levenshtein, Jaccard)
4. **Graph Clustering** - Merge connected components into golden entities

### Phase 2: Transactional Feature Engineering
- Customer-Transaction graph construction
- Node features (volume, frequency, velocity)
- Edge features (shared accounts, cross-border flows, hidden networks)

### Phase 3: AML/Fraud Detection
- **Structuring/Smurfing** - Multiple small transactions just under reporting thresholds
- **Money Mule Networks** - Rapid pass-through of funds to high-risk entities
- **Rapid Velocity/Phantom Profiles** - Same device/IP across multiple resolved profiles in short time windows

## Project Structure

```
FinCrime_Transaction_Graph/
├── docs/                    # Architecture documentation and diagrams
├── src/
│   ├── er/                  # Entity Resolution modules
│   │   ├── standardize.py   # Data cleaning/normalization
│   │   ├── blocking.py      # Blocking/indexing strategies
│   │   ├── matching.py      # Fuzzy matching logic
│   │   └── clustering.py    # Graph clustering to golden entities
│   ├── features/            # Feature engineering
│   │   └── graph_features.py
│   ├── detection/           # AML/Fraud detection
│   │   └── heuristics.py
│   └── bigquery/            # BigQuery integration
├── bigquery/                # BigQuery schemas, DDL, DML, ETL
├── sql/                     # SQL detection functions
├── web/                     # PHP web GUI
├── install/                 # Installation scripts
├── data/                    # Data directories for ETL
└── tests/                   # Unit tests
```

## Quick Start

### Installation
```bash
./install.sh
```

### Python Usage
```python
from src.er.pipeline import EntityResolutionPipeline
from src.detection.heuristics import AMLFraudDetector

# Run ER pipeline
pipeline = EntityResolutionPipeline()
resolved_customers, golden_entities = pipeline.resolve(customers_df, transactions_df)

# Detect suspicious patterns
detector = AMLFraudDetector(resolved_customers, transactions_df)
alerts = detector.run_all_detections()
```

### BigQuery Usage
```python
from src.bigquery.bq_er_pipeline import BigQueryERPipeline

bq_er = BigQueryERPipeline(match_threshold=0.75)
resolved, golden = bq_er.run_with_historical_data(days_back=365)
```

### Web GUI
```bash
cd web
php -S localhost:8080
```
Open `http://localhost:8080` in your browser.

## Requirements

- Python 3.9+
- networkx
- pandas
- numpy
- python-Levenshtein
- jellyfish (for phonetic algorithms)
- scikit-learn
- google-cloud-bigquery
- google-cloud-storage
- pyarrow
- db-dtypes

See `requirements.txt` for full dependencies.

## ETL Process

Files are processed from `data/incoming/` using the ETL pipeline:
```bash
cd /path/to/FinCrime_Transaction_Graph
source venv/bin/activate
python bigquery/etl/run_etl.py
```

Files are automatically moved to `data/loaded/`, `data/rejected/`, or `data/unloaded/` with full validation and duplicate prevention.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Detailed system design
- [BigQuery Guide](bigquery/README.md) - BigQuery integration
- [Installation](install/README.md) - Installation instructions
- [Web GUI Guide](install/WEB_GUI_GUIDE.md) - Web interface usage
- [ETL Quickstart](bigquery/etl/QUICKSTART_ETL.md) - ETL process

## License

See LICENSE file for details.
