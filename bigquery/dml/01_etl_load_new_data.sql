-- ETL: Load New Data from Staging/External Sources

-- Merge new customers into raw_customers
MERGE `your-project-id.fincrime_er.raw_customers` T
USING (
  SELECT 
    customer_id,
    name,
    dob,
    address,
    phone,
    email,
    ssn,
    zip,
    device_id,
    ip_address,
    location,
    source_system,
    CURRENT_DATE() as load_date,
    CURRENT_TIMESTAMP() as load_timestamp,
    GENERATE_UUID() as batch_id
  FROM `your-project-id.fincrime_er.staging_new_customers`
  WHERE load_processed = FALSE
) S
ON T.customer_id = S.customer_id AND T.source_system = S.source_system
WHEN MATCHED THEN
  UPDATE SET
    name = S.name,
    dob = S.dob,
    address = S.address,
    phone = S.phone,
    email = S.email,
    ssn = S.ssn,
    zip = S.zip,
    device_id = S.device_id,
    ip_address = S.ip_address,
    location = S.location,
    load_timestamp = S.load_timestamp
WHEN NOT MATCHED THEN
  INSERT (customer_id, name, dob, address, phone, email, ssn, zip, device_id, ip_address, location, source_system, load_date, load_timestamp, batch_id)
  VALUES (S.customer_id, S.name, S.dob, S.address, S.phone, S.email, S.ssn, S.zip, S.device_id, S.ip_address, S.location, S.source_system, S.load_date, S.load_timestamp, S.batch_id);

-- Merge new transactions into raw_transactions
MERGE `your-project-id.fincrime_er.raw_transactions` T
USING (
  SELECT 
    transaction_id,
    sender_id,
    receiver_id,
    amount,
    currency,
    timestamp,
    DATE(timestamp) as transaction_date,
    channel,
    location,
    transaction_type,
    beneficiary_account,
    source_system,
    CURRENT_DATE() as load_date,
    CURRENT_TIMESTAMP() as load_timestamp,
    GENERATE_UUID() as batch_id
  FROM `your-project-id.fincrime_er.staging_new_transactions`
  WHERE load_processed = FALSE
) S
ON T.transaction_id = S.transaction_id
WHEN MATCHED THEN
  UPDATE SET
    amount = S.amount,
    timestamp = S.timestamp
WHEN NOT MATCHED THEN
  INSERT (transaction_id, sender_id, receiver_id, amount, currency, timestamp, transaction_date, channel, location, transaction_type, beneficiary_account, source_system, load_date, load_timestamp, batch_id)
  VALUES (S.transaction_id, S.sender_id, S.receiver_id, S.amount, S.currency, S.timestamp, S.transaction_date, S.channel, S.location, S.transaction_type, S.beneficiary_account, S.source_system, S.load_date, S.load_timestamp, S.batch_id);

-- Mark staging records as processed
UPDATE `your-project-id.fincrime_er.staging_new_customers`
SET load_processed = TRUE, processed_timestamp = CURRENT_TIMESTAMP()
WHERE load_processed = FALSE;

UPDATE `your-project-id.fincrime_er.staging_new_transactions`
SET load_processed = TRUE, processed_timestamp = CURRENT_TIMESTAMP()
WHERE load_processed = FALSE;
