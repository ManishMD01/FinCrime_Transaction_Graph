#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph')
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph/src')
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph/bigquery')

from src.bigquery.bq_er_pipeline import BigQueryERPipeline
from src.features.graph_features import TransactionGraphBuilder
from src.detection.heuristics import AMLFraudDetector

job_id = sys.argv[1]
days_back = sys.argv[2]
threshold = float(sys.argv[3])
results_dir = sys.argv[4]

try:
    bq_er = BigQueryERPipeline(match_threshold=threshold)
    
    if days_back == 'all':
        resolved_customers, golden_entities = bq_er.run_with_historical_data(days_back=36500)
        transactions_df = bq_er.bq_client.get_historical_transactions(36500)
    else:
        resolved_customers, golden_entities = bq_er.run_with_historical_data(days_back=int(days_back))
        transactions_df = bq_er.bq_client.get_historical_transactions(int(days_back))
    
    if resolved_customers is None:
        resolved_customers = pd.DataFrame()
    if golden_entities is None:
        golden_entities = pd.DataFrame()
    if transactions_df is None:
        transactions_df = pd.DataFrame()
    
    if len(resolved_customers) == 0:
        summary = {
            'job_id': job_id,
            'status': 'success',
            'mode': 'bigquery',
            'days_back': days_back,
            'total_customers': 0,
            'golden_entities': 0,
            'total_transactions': len(transactions_df),
            'graph_nodes': 0,
            'graph_edges': 0,
            'total_alerts': 0
        }
        with open(os.path.join(results_dir, f'{job_id}_summary.json'), 'w') as f:
            json.dump(summary, f, indent=2)
        resolved_customers.to_csv(os.path.join(results_dir, f'{job_id}_resolved_customers.csv'), index=False)
        golden_entities.to_csv(os.path.join(results_dir, f'{job_id}_golden_entities.csv'), index=False)
        pd.DataFrame().to_csv(os.path.join(results_dir, f'{job_id}_node_features.csv'), index=False)
        pd.DataFrame().to_csv(os.path.join(results_dir, f'{job_id}_edge_features.csv'), index=False)
        pd.DataFrame().to_csv(os.path.join(results_dir, f'{job_id}_alerts.csv'), index=False)
        print('SUCCESS')
        sys.exit(0)
    
    graph_builder = TransactionGraphBuilder(resolved_customers, transactions_df)
    graph = graph_builder.build_graph()
    try:
        node_features = graph_builder.extract_node_features()
    except:
        node_features = pd.DataFrame()
    try:
        edge_features = graph_builder.extract_edge_features()
    except:
        edge_features = pd.DataFrame()
    
    detector = AMLFraudDetector(resolved_customers, transactions_df)
    alerts_df = detector.run_all_detections()
    
    resolved_customers.to_csv(os.path.join(results_dir, f'{job_id}_resolved_customers.csv'), index=False)
    golden_entities.to_csv(os.path.join(results_dir, f'{job_id}_golden_entities.csv'), index=False)
    node_features.to_csv(os.path.join(results_dir, f'{job_id}_node_features.csv'), index=False)
    edge_features.to_csv(os.path.join(results_dir, f'{job_id}_edge_features.csv'), index=False)
    alerts_df.to_csv(os.path.join(results_dir, f'{job_id}_alerts.csv'), index=False)
    
    summary = {
        'job_id': job_id,
        'status': 'success',
        'mode': 'bigquery',
        'days_back': days_back,
        'total_customers': len(resolved_customers),
        'golden_entities': len(golden_entities),
        'total_transactions': len(transactions_df),
        'graph_nodes': graph.number_of_nodes(),
        'graph_edges': graph.number_of_edges(),
        'total_alerts': len(alerts_df)
    }
    
    with open(os.path.join(results_dir, f'{job_id}_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print('SUCCESS')
    
except Exception as e:
    import traceback
    error_summary = {
        'job_id': job_id,
        'status': 'error',
        'error': str(e),
        'traceback': traceback.format_exc()
    }
    with open(os.path.join(results_dir, f'{job_id}_summary.json'), 'w') as f:
        json.dump(error_summary, f, indent=2)
    print('ERROR:', e)
    sys.exit(1)
