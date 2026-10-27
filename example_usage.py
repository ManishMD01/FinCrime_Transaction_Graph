#!/usr/bin/env python3
"""
Example usage of the FinCrime Entity Resolution Engine
Demonstrates all three phases of the pipeline.
"""

import pandas as pd
from src.er.pipeline import EntityResolutionPipeline
from src.features.graph_features import TransactionGraphBuilder
from src.detection.heuristics import AMLFraudDetector


def main():
    # Sample Customer Profiles
    customers = pd.DataFrame({
        'customer_id': [1, 2, 3, 4, 5, 6, 7, 8],
        'name': ['John A Smith', 'Jon Smith', 'J. Smith', 'Jane Doe', 
                 'Robert Johnson', 'Bob Johnson', 'Alice Williams', 'Mike Brown'],
        'dob': ['1980-01-01', '1980-01-01', '1980-01-01', '1990-05-05',
                '1975-03-15', '1975-03-15', '1985-07-20', '1982-11-10'],
        'address': ['123 Main St, NY', '123 Main Street New York', '123 Main St',
                    '456 Oak Ave, CA', '789 Pine Rd, TX', '789 Pine Road TX',
                    '321 Elm St, FL', '654 Maple Dr, WA'],
        'phone': ['555-123-4567', '5551234567', '(555) 123-4567', '555-999-8888',
                  '555-444-3333', '5554443333', '555-777-6666', '555-222-1111'],
        'email': ['john.smith@gmail.com', 'jsmith@gmail.com', 'john@example.com', 
                  'jane.doe@yahoo.com', 'robert.j@company.com', 'bobj@gmail.com',
                  'alice.w@gmail.com', 'mike.brown@gmail.com'],
        'ssn': ['123-45-6789', '123-45-6789', '123456789', '987-65-4321',
                '555-66-7777', '555-66-7777', '111-22-3333', '444-55-6666'],
        'zip': ['10001', '10001', '10001', '90210', '77001', '77001', '33101', '98101'],
        'device_id': ['DEV_A1', 'DEV_A1', 'DEV_A1', 'DEV_B2', 'DEV_C3', 'DEV_C3', 'DEV_D4', 'DEV_E5'],
        'ip_address': ['192.168.1.100', '192.168.1.100', '192.168.1.100', '10.0.0.50',
                       '172.16.0.10', '172.16.0.10', '192.168.2.200', '10.1.1.1'],
        'location': ['NY', 'NY', 'NY', 'CA', 'TX', 'TX', 'FL', 'WA']
    })
    
    # Sample Transaction Logs
    transactions = pd.DataFrame({
        'transaction_id': list(range(2001, 2021)),
        'sender_id': [1, 1, 1, 1, 1,  # Structuring pattern
                      5, 6,  # Money mule pattern
                      7, 7, 7, 7, 7,  # Velocity pattern
                      2, 3, 4, 8, 1, 5],
        'receiver_id': [4, 4, 4, 4, 4,
                        7, 7,
                        5, 6, 1, 2, 4,
                        6, 5, 5, 7, 8, 2],
        'amount': [9500, 9400, 9600, 9300, 9800,  # Just below 10k
                   15000, 14000,  # Mule receives
                   2000, 2100, 1900, 2200, 2300,  # Rapid velocity
                   3000, 4000, 5000, 6000, 1000, 2000],
        'timestamp': pd.date_range('2024-01-01 08:00:00', periods=20, freq='2H'),
        'channel': ['wire'] * 5 + ['ach'] * 2 + ['online'] * 5 + ['wire'] * 8,
        'location': ['NY'] * 5 + ['TX'] * 2 + ['FL'] * 5 + ['NY', 'TX', 'CA', 'WA', 'NY', 'TX'],
        'transaction_type': ['transfer'] * 20
    })
    
    print("=" * 80)
    print("PHASE 1: ENTITY RESOLUTION")
    print("=" * 80)
    
    pipeline = EntityResolutionPipeline(match_threshold=0.75)
    resolved_customers, golden_entities = pipeline.resolve(customers, transactions)
    
    print("\nResolved Customers:")
    print(resolved_customers[['customer_id', 'name', 'golden_entity_id']].to_string())
    
    print("\nGolden Entities:")
    print(golden_entities.to_string())
    
    print("\n" + "=" * 80)
    print("PHASE 2: TRANSACTIONAL FEATURE ENGINEERING & GRAPH ANALYTICS")
    print("=" * 80)
    
    graph_builder = TransactionGraphBuilder(resolved_customers, transactions)
    graph = graph_builder.build_graph()
    print(f"\nGraph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    
    node_features = graph_builder.extract_node_features()
    print("\nNode Features (Golden Entities):")
    print(node_features.to_string())
    
    edge_features = graph_builder.extract_edge_features()
    print("\nEdge Features:")
    print(edge_features.to_string())
    
    hidden_networks = graph_builder.find_hidden_networks()
    print(f"\nHidden Networks Found: {len(hidden_networks)}")
    for net in hidden_networks:
        print(f"  - {net['type']}: {net['entities']} (size {net['size']})")
    
    print("\n" + "=" * 80)
    print("PHASE 3: FRAUD & AML DETECTION")
    print("=" * 80)
    
    detector = AMLFraudDetector(resolved_customers, transactions)
    alerts_df = detector.run_all_detections()
    
    print("\nAlerts Generated:")
    if len(alerts_df) > 0:
        print(alerts_df.to_string())
    else:
        print("No alerts generated")
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    main()
