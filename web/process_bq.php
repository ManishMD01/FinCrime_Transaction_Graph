<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index_bq.php');
    exit;
}

$daysBack = $_POST['days_back'] ?? '365';
$threshold = $_POST['threshold'] ?? '0.75';
$jobId = uniqid('job_bq_');
$resultsDir = 'results/';
if (!is_dir($resultsDir)) mkdir($resultsDir, 0755, true);

$pythonScript = "/home/pritsingh000/Git/FinCrime_Transaction_Graph/web/run_fix.php";
$scriptContent = <<<'PYEOF'
#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph')

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
    
    graph_builder = TransactionGraphBuilder(resolved_customers, transactions_df)
    graph = graph_builder.build_graph()
    node_features = graph_builder.extract_node_features()
    try:
        edge_features = graph_builder.extract_edge_features()
    except:
        edge_features = pd.DataFrame()
    if isinstance(edge_features, tuple):
        edge_features = edge_features[0] if len(edge_features) > 0 else pd.DataFrame()
    hidden_networks = graph_builder.find_hidden_networks()
    
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
    error_summary = {
        'job_id': job_id,
        'status': 'error',
        'error': str(e)
    }
    with open(os.path.join(results_dir, f'{job_id}_summary.json'), 'w') as f:
        json.dump(error_summary, f, indent=2)
    print('ERROR:', e)
    sys.exit(1)
PYEOF;

file_put_contents($pythonScript, $scriptContent);
chmod($pythonScript, 0755);

$cmd = "cd /home/pritsingh000/Git/FinCrime_Transaction_Graph && PYTHONPATH=/home/pritsingh000/Git/FinCrime_Transaction_Graph:/home/pritsingh000/Git/FinCrime_Transaction_Graph/src:/home/pritsingh000/Git/FinCrime_Transaction_Graph/bigquery /home/pritsingh000/Git/FinCrime_Transaction_Graph/venv/bin/python " . escapeshellarg($pythonScript) . " " . 
       escapeshellarg($jobId) . " " . 
       escapeshellarg($daysBack) . " " . 
       escapeshellarg($threshold) . " " . 
       escapeshellarg($resultsDir) . " 2>&1";

exec($cmd, $output, $returnCode);
@unlink($pythonScript);

if ($returnCode === 0) {
    $_SESSION['job_id'] = $jobId;
    header('Location: results.php?job_id=' . $jobId);
} else {
    echo "<h2>Error Processing from BigQuery</h2><pre>" . implode("\n", $output) . "</pre>";
    echo "<a href='index_bq.php'>Go Back</a>";
}
?>

// Additional error handling
