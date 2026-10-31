# FinCrime Entity Resolution (ER) & Transaction Graph Engine

High-performance Entity Resolution (ER) engine for Financial Crime Compliance, Anti-Money Laundering (AML), and Fraud Detection. Connects disjointed customer profiles, builds unified golden entities, and flags suspicious transactional patterns.

## Features
- **Entity Resolution**: Data standardization, blocking, fuzzy matching (Jaro-Winkler, Levenshtein), graph clustering
- **Transaction Graph Analytics**: Customer-transaction graph with node/edge features and hidden network detection
- **AML/Fraud Detection**: Structuring/Smurfing, Money Mule Networks, Rapid Velocity/Phantom Profiles
- **BigQuery Integration**: All data stored and processed in Google BigQuery
- **Web GUI**: PHP dashboard for search, investigation, and alerts
- **ETL Pipeline**: File-based ingestion with validation, duplicate prevention, and tracking

## Quick Start

### Installation
```bash
./install.sh
```

### Setup
```bash
source venv/bin/activate
# Configure BigQuery
nano bigquery/config/.env
# Create tables
python bigquery/etl/setup_bigquery.py
```

### ETL Data Loading
Drop CSV files in `data/incoming/`:
- `customers.csv`
- `transactions.csv`

Run ETL:
```bash
python bigquery/etl/run_etl.py
```

### Web GUI
```bash
cd web
php -S localhost:8080
```
Access: `http://localhost:8080`

├── src/er/          # Entity Resolution (standardize, blocking, matching, clustering)
├── src/features/    # Graph features
├── src/detection/   # AML/Fraud heuristics
├── src/bigquery/    # BigQuery integration
├── bigquery/        # Schemas, DDL, DML, ETL scripts
├── web/             # PHP GUI
├── install/         # Installation scripts
├── data/            # Data directories (incoming, loaded, rejected)
└── sql/             # BigQuery SQL views
```

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [BigQuery Guide](bigquery/README.md)
- [ETL Guide](bigquery/etl/QUICKSTART_ETL.md)
- [Web GUI Guide](install/WEB_GUI_GUIDE.md)
- [Installation](install/README.md)
