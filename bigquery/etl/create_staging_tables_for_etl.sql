-- Create staging tables for new data ETL

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.staging_new_customers` (
  customer_id STRING,
  name STRING,
  dob DATE,
  address STRING,
  phone STRING,
  email STRING,
  ssn STRING,
  zip STRING,
  device_id STRING,
  ip_address STRING,
  location STRING,
  source_system STRING,
  load_date DATE,
  load_timestamp TIMESTAMP,
  batch_id STRING,
  load_processed BOOLEAN DEFAULT FALSE,
  processed_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.staging_new_transactions` (
  transaction_id STRING,
  sender_id STRING,
  receiver_id STRING,
  amount NUMERIC,
  currency STRING,
  timestamp TIMESTAMP,
  channel STRING,
  location STRING,
  transaction_type STRING,
  beneficiary_account STRING,
  source_system STRING,
  load_date DATE,
  load_timestamp TIMESTAMP,
  batch_id STRING,
  load_processed BOOLEAN DEFAULT FALSE,
  processed_timestamp TIMESTAMP
);
