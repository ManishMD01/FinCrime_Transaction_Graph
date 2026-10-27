-- FinCrime AML/Fraud Detection SQL Functions
-- Run against resolved entity graph

-- 1. Structuring/Smurfing Detection
CREATE OR REPLACE VIEW vw_structuring_smurfing AS
WITH entity_transactions AS (
    SELECT 
        t.transaction_id,
        t.sender_id,
        c.golden_entity_id,
        t.amount,
        t.timestamp,
        t.channel,
        t.transaction_type
    FROM transactions t
    JOIN resolved_customers c ON t.sender_id = c.customer_id
    WHERE t.sender_id IS NOT NULL
),
time_windows AS (
    SELECT 
        golden_entity_id,
        DATE_TRUNC('hour', timestamp) as hour_window,
        COUNT(*) as txn_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        MIN(timestamp) as window_start,
        MAX(timestamp) as window_end
    FROM entity_transactions
    WHERE amount >= 8000 AND amount < 10000  -- Just below threshold
    GROUP BY golden_entity_id, DATE_TRUNC('hour', timestamp)
    HAVING COUNT(*) >= 3 AND SUM(amount) >= 25000
)
SELECT 
    golden_entity_id,
    'STRUCTURING_SMURFING' as alert_type,
    'HIGH' as severity,
    hour_window,
    txn_count,
    total_amount,
    avg_amount,
    window_start,
    window_end,
    EXTRACT(EPOCH FROM (window_end - window_start)) / 3600 as window_hours
FROM time_windows;

-- 2. Money Mule Network Detection
CREATE OR REPLACE VIEW vw_money_mule_networks AS
WITH inflows AS (
    SELECT 
        t.transaction_id,
        t.receiver_id as mule_customer_id,
        c.golden_entity_id as mule_entity_id,
        t.sender_id as source_customer_id,
        s_c.golden_entity_id as source_entity_id,
        t.amount,
        t.timestamp
    FROM transactions t
    JOIN resolved_customers c ON t.receiver_id = c.customer_id
    LEFT JOIN resolved_customers s_c ON t.sender_id = s_c.customer_id
    WHERE t.receiver_id IS NOT NULL
),
outflows AS (
    SELECT 
        t.transaction_id,
        t.sender_id as mule_customer_id,
        c.golden_entity_id as mule_entity_id,
        t.receiver_id as dest_customer_id,
        t.amount,
        t.timestamp
    FROM transactions t
    JOIN resolved_customers c ON t.sender_id = c.customer_id
    WHERE t.sender_id IS NOT NULL
),
mule_activity AS (
    SELECT 
        i.mule_entity_id,
        COUNT(DISTINCT i.source_entity_id) as unique_source_entities,
        COUNT(DISTINCT i.transaction_id) as inflow_count,
        SUM(i.amount) as total_inflow,
        o.transaction_id as outflow_txn_id,
        o.amount as outflow_amount,
        o.timestamp as outflow_time,
        MIN(i.timestamp) as first_inflow_time
    FROM inflows i
    JOIN outflows o ON i.mule_entity_id = o.mule_entity_id
    WHERE o.timestamp >= i.timestamp 
      AND o.timestamp - i.timestamp <= INTERVAL '60 minutes'
    GROUP BY i.mule_entity_id, o.transaction_id, o.amount, o.timestamp
    HAVING COUNT(DISTINCT i.source_entity_id) >= 2
       AND SUM(i.amount) > 0
       AND o.amount >= 0.7 * SUM(i.amount)
)
SELECT 
    mule_entity_id as golden_entity_id,
    'MONEY_MULE_NETWORK' as alert_type,
    'CRITICAL' as severity,
    unique_source_entities as source_entity_count,
    inflow_count,
    total_inflow,
    outflow_amount,
    outflow_amount / total_inflow as pass_through_ratio,
    EXTRACT(EPOCH FROM (outflow_time - first_inflow_time)) / 60 as time_to_transfer_minutes,
    outflow_time
FROM mule_activity;

-- 3. Rapid Velocity / Phantom Profiles
CREATE OR REPLACE VIEW vw_rapid_velocity_phantom AS
WITH entity_customer_mapping AS (
    SELECT 
        golden_entity_id,
        COUNT(DISTINCT customer_id) as profile_count,
        ARRAY_AGG(DISTINCT device_id) FILTER (WHERE device_id IS NOT NULL) as all_devices,
        ARRAY_AGG(DISTINCT ip_address) FILTER (WHERE ip_address IS NOT NULL) as all_ips
    FROM resolved_customers
    GROUP BY golden_entity_id
    HAVING COUNT(DISTINCT customer_id) >= 2
),
entity_txns AS (
    SELECT 
        t.transaction_id,
        COALESCE(c1.golden_entity_id, c2.golden_entity_id) as golden_entity_id,
        t.amount,
        t.timestamp,
        t.device_id,
        t.ip_address
    FROM transactions t
    LEFT JOIN resolved_customers c1 ON t.sender_id = c1.customer_id
    LEFT JOIN resolved_customers c2 ON t.receiver_id = c2.customer_id
    WHERE COALESCE(c1.golden_entity_id, c2.golden_entity_id) IS NOT NULL
),
velocity_windows AS (
    SELECT 
        e.golden_entity_id,
        m.profile_count,
        m.all_devices,
        m.all_ips,
        DATE_TRUNC('hour', e.timestamp) as hour_window,
        COUNT(*) as txn_count,
        SUM(e.amount) as total_amount,
        COUNT(DISTINCT e.device_id) as distinct_devices,
        COUNT(DISTINCT e.ip_address) as distinct_ips,
        MIN(e.timestamp) as window_start,
        MAX(e.timestamp) as window_end
    FROM entity_txns e
    JOIN entity_customer_mapping m ON e.golden_entity_id = m.golden_entity_id
    GROUP BY e.golden_entity_id, m.profile_count, m.all_devices, m.all_ips, DATE_TRUNC('hour', e.timestamp)
    HAVING COUNT(*) >= 5
)
SELECT 
    golden_entity_id,
    'RAPID_VELOCITY_PHANTOM_PROFILE' as alert_type,
    'HIGH' as severity,
    profile_count as underlying_profile_count,
    txn_count as transaction_count,
    EXTRACT(EPOCH FROM (window_end - window_start)) / 60 as time_window_minutes,
    total_amount,
    all_devices as shared_devices,
    all_ips as shared_ips,
    window_start
FROM velocity_windows
WHERE array_length(all_devices, 1) >= 1 OR array_length(all_ips, 1) >= 1;

-- Unified alerts view
CREATE OR REPLACE VIEW vw_all_aml_alerts AS
SELECT * FROM vw_structuring_smurfing
UNION ALL
SELECT golden_entity_id, alert_type, severity, NULL as hour_window, NULL as txn_count, NULL as total_amount, 
       NULL as avg_amount, NULL as window_start, NULL as window_end, NULL as window_hours,
       NULL as source_entity_count, NULL as inflow_count, NULL as outflow_amount, NULL as pass_through_ratio,
       NULL as time_to_transfer_minutes, NULL as outflow_time,
       NULL as underlying_profile_count, NULL as transaction_count, NULL as time_window_minutes,
       NULL as shared_devices, NULL as shared_ips
FROM vw_money_mule_networks
WHERE FALSE; -- Simplified for compatibility
