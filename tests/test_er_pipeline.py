"""
Tests for Entity Resolution Pipeline
"""

import pandas as pd
from src.er.pipeline import EntityResolutionPipeline


def test_er_pipeline():
    """Test basic ER pipeline functionality."""
    # Create sample customer data
    customers = pd.DataFrame({
        'customer_id': [1, 2, 3, 4],
        'name': ['John Smith', 'Jon Smith', 'Jane Doe', 'John Smith'],
        'dob': ['1980-01-01', '1980-01-01', '1990-05-05', '1980-01-01'],
        'address': ['123 Main St', '123 Main Street', '456 Oak Ave', '123 Main St'],
        'phone': ['555-123-4567', '5551234567', '555-999-8888', '555-123-4567'],
        'email': ['john@example.com', 'john@example.com', 'jane@example.com', 'john.smith@example.com'],
        'ssn': ['123-45-6789', '123-45-6789', '987-65-4321', '123-45-6789'],
        'zip': ['12345', '12345', '54321', '12345'],
        'device_id': ['DEV001', 'DEV001', 'DEV002', 'DEV003'],
        'ip_address': ['1.2.3.4', '1.2.3.4', '5.6.7.8', '9.9.9.9'],
        'location': ['NY', 'NY', 'CA', 'NY']
    })
    
    transactions = pd.DataFrame({
        'transaction_id': [101, 102, 103],
        'sender_id': [1, 3, 4],
        'receiver_id': [3, 1, 2],
        'amount': [5000, 3000, 2000],
        'timestamp': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00'],
        'channel': ['online', 'atm', 'wire'],
        'location': ['NY', 'CA', 'NY'],
        'transaction_type': ['transfer', 'withdrawal', 'transfer']
    })
    
    pipeline = EntityResolutionPipeline(match_threshold=0.75)
    resolved_customers, golden_entities = pipeline.resolve(customers, transactions)
    
    # Customer 1, 2, 4 should be clustered together (same SSN, similar name, same address/phone)
    cluster_1 = resolved_customers[resolved_customers['customer_id'].isin([1, 2, 4])]['golden_entity_id'].unique()
    assert len(cluster_1) == 1, "Customers 1,2,4 should be in same golden entity"
    
    print("Test passed!")
    return resolved_customers, golden_entities


if __name__ == '__main__':
    test_er_pipeline()
