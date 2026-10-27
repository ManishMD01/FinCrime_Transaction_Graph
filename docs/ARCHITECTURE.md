# FinCrime Entity Resolution Engine - Architecture

## Executive Summary

This document outlines the architecture for a high-performance Entity Resolution (ER) Engine designed for Financial Crime Compliance, AML, and Fraud Detection. The system connects disjointed customer profiles and flags suspicious transactional patterns across resolved entities.

## 1. Entity Resolution Architecture

### 1.1 Data Standardization
**Purpose:** Parse, clean, and normalize heterogeneous data from multiple sources.

**Components:**
- **Name Standardization:** Tokenization, prefix/suffix removal, phonetic encoding (Soundex, Metaphone)
- **Address Standardization:** Abbreviation normalization (Street→St, Avenue→Ave), parsing of components
- **Contact Standardization:** Phone number formatting (E.164 normalization), email normalization (gmail.com dot removal)
- **ID Standardization:** SSN/National ID cleaning (digit extraction)
- **Geographic Standardization:** ZIP code extraction and validation

**Implementation:** `src/er/standardize.py`

### 1.2 Blocking / Indexing
**Purpose:** Prevent O(N²) combinatorial explosion by creating candidate pairs.

**Strategies:**
- **Phonetic Blocking:** Soundex and Metaphone on normalized names
- **Geographic Blocking:** ZIP code clustering
- **Contact Blocking:** Exact match on standardized phone numbers
- **Temporal Blocking:** Date of birth matching
- **Device Blocking:** Shared Device ID correlation
- **Composite Blocking:** Union of all blocking strategies

**Performance:** Typically reduces pairs by 99%+ while maintaining high recall.

**Implementation:** `src/er/blocking.py`

### 1.3 Record Linkage (Fuzzy Matching)
**Purpose:** Determine if candidate pairs represent the same entity.

**Deterministic Rules (High Confidence):**
- Exact match on National ID/SSN with matching name → Auto-match (score 1.0)

**Probabilistic Matching:**
| Attribute | Algorithm | Weight | Rationale |
|-----------|-----------|--------|-----------|
| SSN/National ID | Exact Match | 30% | Strongest identifier |
| Name | Jaro-Winkler | 20% | Handles typos, nicknames, order variations |
| Phone | Exact Match | 15% | Often stable identifier |
| Email | Exact Match | 12% | Digital identifier |
| Date of Birth | Exact Match | 10% | Strong demographic match |
| Address | Levenshtein | 8% | Handles formatting differences |
| ZIP Code | Exact Match | 3% | Geographic proximity |
| Device ID/IP | Exact Match | 2% | Digital footprint correlation |

**Match Threshold:** Default 0.75 (tunable based on precision/recall requirements)

**Implementation:** `src/er/matching.py`

### 1.4 Graph Clustering
**Purpose:** Merge resolved records into single "Golden Entity".

**Approach:**
1. Build undirected graph where nodes = customer records, edges = matches (score ≥ threshold)
2. Find connected components using NetworkX `connected_components()`
3. All records in a component merge into one Golden Entity
4. Create consolidated golden entity with best/most complete attributes

**Benefits:**
- Transitive closure: If A matches B and B matches C, all three cluster together
- Handles complex multi-way matches
- Scalable to millions of records

**Implementation:** `src/er/clustering.py`

## 2. Transactional Feature Engineering & Graph Analytics

### 2.1 Unified Customer-Transaction Graph
Build a directed graph where:
- **Nodes:** Golden Entities (resolved customers)
- **Edges:** Aggregated transactions between entities
- **Edge Attributes:** Total amount, count, channels, timestamps

### 2.2 Node Features
| Feature | Description | Use Case |
|---------|-------------|----------|
| `total_volume` | Sum of all inflows + outflows | Overall activity level |
| `total_inflow/outflow` | Directional volumes | Net flow analysis |
| `transaction_frequency` | Total transaction count | Activity intensity |
| `velocity_txns_per_hour` | Transactions per hour in active period | Velocity detection |
| `avg/max_transaction_amount` | Amount statistics | Pattern analysis |
| `unique_counterparties` | Distinct entities transacted with | Network breadth |
| `member_count` | Number of profiles merged | Phantom profile indicator |

### 2.3 Edge Features
| Feature | Description | Use Case |
|---------|-------------|----------|
| `total_amount` | Aggregated flow between entities | Relationship strength |
| `transaction_count` | Number of transactions | Interaction frequency |
| `avg_amount` | Average transaction size | Pattern identification |
| `cross_border` | Different locations | Cross-border risk |
| `shared_accounts` | Common account relationships | Hidden connections |

### 2.4 Hidden Network Detection
- **Strongly Connected Components:** Circular money flows
- **Cliques:** Tightly interconnected groups
- **Community Detection:** Identify suspicious clusters

**Implementation:** `src/features/graph_features.py`

## 3. Fraud & AML Detection Heuristics

### 3.1 Structuring / Smurfing
**Pattern:** Breaking large transactions into multiple smaller amounts just below regulatory reporting thresholds.

**Detection Logic:**
```python
- Group transactions by sender golden entity
- Look for clusters of transactions in time window (e.g., 24 hours)
- Flag if: count >= 3 AND amounts between 80-99% of threshold AND total >= threshold
- Typical threshold: $10,000 (CTR filing requirement in US)
```

**Red Flags:** Consistent amounts, structured timing, avoidance behavior

### 3.2 Money Mule Networks
**Pattern:** Entity receives funds from multiple unlinked sources and rapidly transfers to high-risk entities.

**Detection Logic:**
```python
- Identify entities receiving from >= 2 different source entities
- Check for outflows within short time window (e.g., 60 minutes)
- Flag if pass-through ratio >= 70% (most funds forwarded quickly)
- Multiple sources + rapid transfer = mule indicator
```

**Red Flags:** No business justification, rapid pass-through, multiple senders

### 3.3 Rapid Velocity / Phantom Profiles
**Pattern:** Multiple distinct customer profiles (resolved as same entity) performing high-frequency transactions from same device/IP.

**Detection Logic:**
```python
- Find golden entities with member_count >= 2 (multiple underlying profiles)
- Check for shared device_id or ip_address across profiles
- Monitor transaction velocity in short windows (e.g., 60 minutes, >= 5 txns)
- Flag as phantom profile / synthetic identity risk
```

**Red Flags:** Identity fragmentation, shared digital footprint, burst activity

**Implementation:** `src/detection/heuristics.py`, `sql/detection_functions.sql`

## Performance Considerations

- **Blocking:** Critical for scalability - use multiple blocking keys
- **Incremental Processing:** Support delta updates for new records
- **Graph Algorithms:** NetworkX efficient enough for 10^6 nodes; consider Neo4j for larger scale
- **Caching:** Cache phonetic codes and standardized values
- **Parallelization:** Embarrassingly parallel for matching pairs

## Security & Compliance

- **PII Handling:** Encrypt sensitive fields, audit logging
- **Data Lineage:** Track all transformations
- **Explainability:** Maintain match scores and reasons for clustering
- **Retention:** Follow regulatory requirements
- **Access Control:** Role-based access to alerts and PII
