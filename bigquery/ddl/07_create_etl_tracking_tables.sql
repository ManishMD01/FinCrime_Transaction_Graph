-- Create ETL Tracking and Validation Tables

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.etl_file_tracking` (
  file_id STRING NOT NULL,
  file_name STRING NOT NULL,
  file_path STRING,
  file_type STRING, -- customers/transactions
  file_hash STRING,
  file_size_bytes INT64,
  rows_count INT64,
  status STRING, -- PENDING/LOADING/LOADED/FAILED/REJECTED
  batch_id STRING,
  source_system STRING,
  loaded_to_table STRING,
  loaded_rows INT64,
  duplicate_rows INT64,
  rejected_rows INT64,
  load_date DATE,
  load_timestamp TIMESTAMP,
  processed_timestamp TIMESTAMP,
  error_message STRING,
  checksum_verified BOOLEAN
)
PARTITION BY load_date
CLUSTER BY file_type, status
OPTIONS(description="Track ETL file processing status");

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.etl_data_validation` (
  validation_id STRING NOT NULL,
  batch_id STRING,
  file_id STRING,
  table_name STRING,
  validation_type STRING,
  validation_rule STRING,
  passed BOOLEAN,
  failed_count INT64,
  total_count INT64,
  failure_details STRING,
  validation_timestamp TIMESTAMP
)
PARTITION BY DATE(validation_timestamp)
CLUSTER BY batch_id, validation_type
OPTIONS(description="Data validation results");

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.etl_loaded_records` (
  record_key STRING NOT NULL,
  table_name STRING,
  source_file_id STRING,
  batch_id STRING,
  customer_id STRING,
  transaction_id STRING,
  load_date DATE,
  load_timestamp TIMESTAMP
)
PARTITION BY load_date
CLUSTER BY table_name, source_file_id
OPTIONS(description="Track individual records to prevent duplicates");
