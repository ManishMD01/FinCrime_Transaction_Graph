-- Standardize Data from Raw to Staging

INSERT INTO `your-project-id.fincrime_er.stg_customers_standardized`
SELECT 
  customer_id,
  name as original_name,
  -- Name standardization (simplified in SQL, full logic in Python)
  LOWER(TRIM(SPLIT(name, ' ')[SAFE_OFFSET(0)])) as first_name,
  LOWER(TRIM(SPLIT(name, ' ')[SAFE_OFFSET(ARRAY_LENGTH(SPLIT(TRIM(name), ' ')) - 1)])) as last_name,
  LOWER(REGEXP_REPLACE(TRIM(name), r'[^a-zA-Z\s]', '')) as full_name_clean,
  -- Phonetic codes would be computed in Python
  '' as soundex,
  '' as metaphone,
  dob as original_dob,
  dob,
  address as original_address,
  LOWER(REGEXP_REPLACE(TRIM(address), r'\bstreet\b', 'st')) as address_clean,
  REGEXP_EXTRACT(address, r'^(\d+)') as street_number,
  REGEXP_REPLACE(address, r'^\d+\s+', '') as street_name,
  zip,
  REGEXP_EXTRACT(zip, r'(\d{5})') as zip_std,
  phone as original_phone,
  REGEXP_REPLACE(phone, r'[^0-9]', '') as phone_std,
  email as original_email,
  LOWER(TRIM(email)) as email_std,
  ssn as original_ssn,
  REGEXP_REPLACE(ssn, r'[^0-9]', '') as ssn_std,
  device_id,
  ip_address,
  location,
  source_system,
  batch_id,
  CURRENT_TIMESTAMP() as standardization_date
FROM `your-project-id.fincrime_er.raw_customers`
WHERE load_date = CURRENT_DATE()
  AND customer_id NOT IN (SELECT customer_id FROM `your-project-id.fincrime_er.stg_customers_standardized`);

-- Enrich transactions
INSERT INTO `your-project-id.fincrime_er.stg_transactions_enriched`
SELECT 
  transaction_id,
  sender_id,
  receiver_id,
  amount,
  COALESCE(currency, 'USD') as currency,
  timestamp,
  transaction_date,
  channel,
  location,
  transaction_type,
  FALSE as is_cross_border, -- Will be computed based on locations
  amount >= 10000 as is_high_amount,
  CASE 
    WHEN amount < 1000 THEN 'SMALL'
    WHEN amount < 10000 THEN 'MEDIUM'
    WHEN amount < 100000 THEN 'LARGE'
    ELSE 'VERY_LARGE'
  END as amount_bucket,
  source_system,
  batch_id,
  CURRENT_TIMESTAMP() as enrichment_date
FROM `your-project-id.fincrime_er.raw_transactions`
WHERE transaction_date = CURRENT_DATE()
  AND transaction_id NOT IN (SELECT transaction_id FROM `your-project-id.fincrime_er.stg_transactions_enriched`);
