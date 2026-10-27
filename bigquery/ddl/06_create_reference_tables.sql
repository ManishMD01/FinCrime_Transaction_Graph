-- Create Reference Data Tables

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.ref_country_codes` (
  country_code STRING NOT NULL,
  country_name STRING,
  iso_alpha3 STRING,
  region STRING,
  is_high_risk BOOLEAN,
  load_date DATE DEFAULT CURRENT_DATE()
)
CLUSTER BY country_code
OPTIONS(description="Country code reference data");

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.ref_currency_codes` (
  currency_code STRING NOT NULL,
  currency_name STRING,
  is_active BOOLEAN,
  load_date DATE DEFAULT CURRENT_DATE()
)
CLUSTER BY currency_code
OPTIONS(description="Currency code reference data");

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.ref_channel_types` (
  channel_code STRING NOT NULL,
  channel_name STRING,
  channel_category STRING,
  is_digital BOOLEAN,
  risk_level STRING,
  load_date DATE DEFAULT CURRENT_DATE()
)
CLUSTER BY channel_code
OPTIONS(description="Transaction channel reference data");

CREATE TABLE IF NOT EXISTS `your-project-id.fincrime_er.ref_transaction_types` (
  transaction_type_code STRING NOT NULL,
  transaction_type_name STRING,
  description STRING,
  risk_weight FLOAT64,
  load_date DATE DEFAULT CURRENT_DATE()
)
CLUSTER BY transaction_type_code
OPTIONS(description="Transaction type reference data");

CREATE TABLE IF NOT tag_exists = FALSE;
