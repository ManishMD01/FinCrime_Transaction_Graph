-- Create Transaction Graph Tables

-- Entity Transaction Graph
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.entity_transaction_graph` (
  edge_id STRING NOT NULL,
  sender_entity_id STRING NOT NULL,
  receiver_entity_id STRING NOT NULL,
  total_amount NUMERIC,
  transaction_count INT64,
  avg_amount NUMERIC,
  first_transaction TIMESTAMP,
  last_transaction TIMESTAMP,
  channels ARRAY<STRING>,
  locations ARRAY<STRING>,
  is_cross_border BOOLEAN,
  shared_accounts BOOLEAN,
  graph_date DATE,
  batch_id STRING
)
PARTITION BY graph_date
CLUSTER BY sender_entity_id, receiver_entity_id
OPTIONS(
  description="Customer-Transaction graph edges between golden entities",
  labels=[("layer", "graph"), ("domain", "fincrime")]
);

-- Entity Node Features
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.entity_features` (
  golden_entity_id STRING NOT NULL,
  total_volume NUMERIC,
  total_inflow NUMERIC,
  total_outflow NUMERIC,
  net_flow NUMERIC,
  transaction_frequency INT64,
  outflow_frequency INT64,
  inflow_frequency INT64,
  avg_transaction_amount NUMERIC,
  max_transaction_amount NUMERIC,
  velocity_txns_per_hour FLOAT64,
  unique_counterparties INT64,
  member_count INT64,
  first_activity_date DATE,
  last_activity_date DATE,
  feature_date DATE,
  batch_id STRING
)
PARTITION BY feature_date
CLUSTER BY golden_entity_id
OPTIONS(
  description="Node features for golden entities",
  labels=[("layer", "graph"), ("domain", "fincrime")]
);

-- Entity Edge Features
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.entity_edge_features` (
  edge_id STRING NOT NULL,
  sender_entity_id STRING NOT NULL,
  receiver_entity_id STRING NOT NULL,
  total_amount NUMERIC,
  transaction_count INT64,
  avg_amount NUMERIC,
  cross_border BOOLEAN,
  shared_accounts BOOLEAN,
  relationship_strength FLOAT64,
  risk_indicator BOOLEAN,
  feature_date DATE,
  batch_id STRING
)
PARTITION BY feature_date
CLUSTER BY sender_entity_id, receiver_entity_id
OPTIONS(
  description="Edge features between golden entities",
  labels=[("layer", "graph"), ("domain", "fincrime")]
);
