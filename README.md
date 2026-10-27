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
│   └── detection/           # AML/Fraud detection
│       └── heuristics.py
├── sql/                     # SQL detection functions
├── tests/                   # Unit tests
└── notebooks/               # Analysis notebooks
```

## Quick Start

```python
from src.er.pipeline import EntityResolutionPipeline
from src.detection.heuristics import AMLFraudDetector

# Run ER pipeline
pipeline = EntityResolutionPipeline()
golden_entities = pipeline.resolve(customers_df, transactions_df)

# Detect suspicious patterns
detector = AMLFraudDetector(golden_entities, transactions_df)
alerts = detector.run_all_detections()
```

## Requirements

- Python 3.9+
- networkx
- pandas
- numpy
- python-Levenshtein
- jellyfish (for phonetic algorithms)
- scikit-learn
- sqlalchemy

See `requirements.txt` for full dependencies.


## Web GUI

A PHP-based web interface is included for easy usage.

### Starting the Server
```bash
cd web
php -S localhost:8080
# Or for remote access: php -S 0.0.0.0:8080
```

### Access
Open `http://localhost:8080` in your browser. No authentication required.

See [install/WEB_GUI_GUIDE.md](install/WEB_GUI_GUIDE.md) for detailed instructions.
