-- Create Resolved Entity Tables

-- Resolved Customers - Mapped to Golden Entities
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.resolved_customers` (
  customer_id STRING NOT NULL,
  golden_entity_id STRING NOT NULL,
  cluster_id INT64,
  match_confidence FLOAT64,
  resolution_method STRING,
  first_name STRING,
  last_name STRING,
  full_name_clean STRING,
  phone_std STRING,
  email_std STRING,
  ssn_std STRING,
  address_clean STRING,
  zip_std STRING,
  device_id STRING,
  ip_address STRING,
  dob DATE,
  location STRING,
  resolution_date TIMESTAMP,
  batch_id STRING
)
PARTITION BY DATE(resolution_date)
CLUSTER BY golden_entity_id, customer_id
OPTIONS(
  description="Customer records mapped to golden entities",
  labels=[("layer", "resolved"), ("domain", "fincrime")]
);

-- Golden Entities - Consolidated Records
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.golden_entities` (
  golden_entity_id STRING NOT NULL,
  member_count INT64,
  member_ids ARRAY<STRING>,
  primary_name STRING,
  primary_phone STRING,
  primary_email STRING,
  primary_address STRING,
  primary_dob DATE,
  all_ssns ARRAY<STRING>,
  all_phones ARRAY<STRING>,
  all_emails ARRAY<STRING>,
  all_devices ARRAY<STRING>,
  all_ips ARRAY<STRING>,
  all_addresses ARRAY<STRING>,
  risk_score FLOAT64,
  risk_category STRING,
  created_date TIMESTAMP,
  last_updated TIMESTAMP,
  batch_id STRING
)
CLUSTER BY golden_entity_id
OPTIONS(
  description="Consolidated golden entity records",
  labels=[("layer", "resolved"), ("domain", "fincrime")]
);
