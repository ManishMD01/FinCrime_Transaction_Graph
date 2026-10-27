-- Create Staging Tables for Standardized Data

-- Staging Customers - Standardized
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.stg_customers_standardized` (
  customer_id STRING NOT NULL,
  original_name STRING,
  first_name STRING,
  last_name STRING,
  full_name_clean STRING,
  soundex STRING,
  metaphone STRING,
  original_dob DATE,
  dob DATE,
  original_address STRING,
  address_clean STRING,
  street_number STRING,
  street_name STRING,
  zip STRING,
  zip_std STRING,
  original_phone STRING,
  phone_std STRING,
  original_email STRING,
  email_std STRING,
  original_ssn STRING,
  ssn_std STRING,
  device_id STRING,
  ip_address STRING,
  location STRING,
  source_system STRING,
  batch_id STRING,
  standardization_date TIMESTAMP
)
PARTITION BY DATE(standardization_date)
CLUSTER BY customer_id, phone_std, email_std
OPTIONS(
  description="Standardized and cleaned customer profiles",
  labels=[("layer", "staging"), ("domain", "fincrime")]
);

-- Staging Transactions - Enriched
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.stg_transactions_enriched` (
  transaction_id STRING NOT NULL,
  sender_id STRING,
  receiver_id STRING,
  amount NUMERIC NOT NULL,
  currency STRING,
  timestamp TIMESTAMP NOT NULL,
  transaction_date DATE NOT NULL,
  channel STRING,
  location STRING,
  transaction_type STRING,
  is_cross_border BOOLEAN,
  is_high_amount BOOLEAN,
  amount_bucket STRING,
  source_system STRING,
  batch_id STRING,
  enrichment_date TIMESTAMP
)
PARTITION BY transaction_date
CLUSTER BY sender_id, receiver_id
OPTIONS(
  description="Enriched transaction data",
  labels=[("layer", "staging"), ("domain", "fincrime")]
);
