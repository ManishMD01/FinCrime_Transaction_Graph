-- Create Raw Tables for Historical and New Data Ingestion

-- Dataset will be created separately or use existing
-- CREATE SCHEMA IF NOT EXISTS `your-project-id.fincrime_er`;

-- Raw Customers Table
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.raw_customers` (
  customer_id STRING NOT NULL OPTIONS(description="Source system customer identifier"),
  name STRING OPTIONS(description="Full name as provided"),
  dob DATE OPTIONS(description="Date of birth"),
  address STRING OPTIONS(description="Address as provided"),
  phone STRING OPTIONS(description="Phone number"),
  email STRING OPTIONS(description="Email address"),
  ssn STRING OPTIONS(description="SSN/National ID"),
  zip STRING OPTIONS(description="ZIP/Postal code"),
  device_id STRING OPTIONS(description="Device identifier"),
  ip_address STRING OPTIONS(description="IP address"),
  location STRING OPTIONS(description="Location/Country"),
  source_system STRING OPTIONS(description="Source system name"),
  load_date DATE NOT NULL OPTIONS(description="ETL load date"),
  load_timestamp TIMESTAMP NOT NULL OPTIONS(description="ETL load timestamp"),
  batch_id STRING OPTIONS(description="Batch identifier")
)
PARTITION BY load_date
CLUSTER BY customer_id
OPTIONS(
  description="Raw customer profile data from source systems",
  labels=[("layer", "raw"), ("domain", "fincrime")]
);

-- Raw Transactions Table
CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.raw_transactions` (
  transaction_id STRING NOT NULL OPTIONS(description="Transaction identifier"),
  sender_id STRING OPTIONS(description="Sender customer ID"),
  receiver_id STRING OPTIONS(description="Receiver customer ID"),
  amount NUMERIC NOT NULL OPTIONS(description="Transaction amount"),
  currency STRING OPTIONS(description="Currency code"),
  timestamp TIMESTAMP NOT NULL OPTIONS(description="Transaction timestamp"),
  transaction_date DATE NOT NULL OPTIONS(description="Transaction date for partitioning"),
  channel STRING OPTIONS(description="Transaction channel"),
  location STRING OPTIONS(description="Transaction location"),
  transaction_type STRING OPTIONS(description="Transaction type"),
  beneficiary_account STRING OPTIONS(description="Beneficiary account"),
  source_system STRING OPTIONS(description="Source system"),
  load_date DATE NOT NULL OPTIONS(description="ETL load date"),
  load_timestamp TIMESTAMP NOT NULL OPTIONS(description="ETL load timestamp"),
  batch_id STRING OPTIONS(description="Batch identifier")
)
PARTITION BY transaction_date
CLUSTER BY sender_id, receiver_id
OPTIONS(
  description="Raw transaction logs from source systems",
  labels=[("layer", "raw"), ("domain", "fincrime")]
);
