<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}

$uploadDir = 'uploads/';
$resultsDir = 'results/';
if (!is_dir($uploadDir)) mkdir($uploadDir, 0755, true);
if (!is_dir($resultsDir)) mkdir($resultsDir, 0755, true);

$threshold = $_POST['threshold'] ?? '0.75';
$jobId = uniqid('job_');

// Upload files
$customersFile = $uploadDir . $jobId . '_customers.csv';
$transactionsFile = $uploadDir . $jobId . '_transactions.csv';

if (move_uploaded_file($_FILES['customers']['tmp_name'], $customersFile) && 
    move_uploaded_file($_FILES['transactions']['tmp_name'], $transactionsFile)) {
    
    // Create Python script to run
    $pythonScript = "run_engine_" . $jobId . ".py";
    $scriptContent = <<<'PYEOF'
#!/usr/bin/env python3
import sys
import os
import json
import pandas as pd
sys.path.insert(0, '/home/pritsingh000/Git/FinCrime_Transaction_Graph')

from src.er.pipeline import EntityResolutionPipeline
from src.features.graph_features import TransactionGraphBuilder
from src.detection.heuristics import AMLFraudDetector

job_id = sys.argv[1]
threshold = float(sys.argv[2])
customers_path = sys.argv[3]
transactions_path = sys.argv[4]
results_dir = sys.argv[5]

try:
    # Load data
    customers = pd.read_csv(customers_path)
    transactions = pd.read_csv(transactions_path)
    
    # Phase 1: Entity Resolution
    pipeline = EntityResolutionPipeline(match_threshold=threshold)
    resolved_customers, golden_entities = pipeline.resolve(customers, transactions)
    
    # Phase 2: Graph Analytics
    graph_builder = TransactionGraphBuilder(resolved_customers, transactions)
    graph = graph_builder.build_graph()
    node_features = graph_builder.extract_node_features()
    edge_features = graph_builder.extract_edge_features()
    hidden_networks = graph_builder.find_hidden_networks()
    
    # Phase 3: Detection
    detector = AMLFraudDetector(resolved_customers, transactions)
    alerts_df = detector.run_all_detections()
    
    # Save results
    resolved_customers.to_csv(os.path.join(results_dir, f'{job_id}_resolved_customers.csv'), index=False)
    golden_entities.to_csv(os.path.join(results_dir, f'{job_id}_golden_entities.csv'), index=False)
    node_features.to_csv(os.path.join(results_dir, f'{job_id}_node_features.csv'), index=False)
    edge_features.to_csv(os.path.join(results_dir, f'{job_id}_edge_features.csv'), index=False)
    alerts_df.to_csv(os.path.join(results_dir, f'{job_id}_alerts.csv'), index=False)
    
    # Save summary
    summary = {
        'job_id': job_id,
        'status': 'success',
        'total_customers': len(customers),
        'total_transactions': len(transactions),
        'golden_entities': len(golden_entities),
        'resolved_clusters': len(resolved_customers['golden_entity_id'].unique()),
        'graph_nodes': graph.number_of_nodes(),
        'graph_edges': graph.number_of_edges(),
        'total_alerts': len(alerts_df),
        'alerts_by_type': alerts_df['alert_type'].value_counts().to_dict() if len(alerts_df) > 0 else {},
        'blocking_stats': pipeline.blocker.get_blocking_statistics() if pipeline.blocker else {},
        'clustering_stats': pipeline.clusterer.get_cluster_statistics() if pipeline.clusterer else {}
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
    
    // Execute Python script
    $cmd = "python3 " . escapeshellarg($pythonScript) . " " . 
           escapeshellarg($jobId) . " " . 
           escapeshellarg($threshold) . " " . 
           escapeshellarg($customersFile) . " " . 
           escapeshellarg($transactionsFile) . " " . 
           escapeshellarg($resultsDir) . " 2>&1";
    
    exec($cmd, $output, $returnCode);
    
    // Clean up script
    @unlink($pythonScript);
    
    if ($returnCode === 0) {
        $_SESSION['job_id'] = $jobId;
        header('Location: results.php?job_id=' . $jobId);
    } else {
        echo "<h2>Error Processing</h2><pre>" . implode("\n", $output) . "</pre>";
        echo "<a href='index.php'>Go Back</a>";
    }
} else {
    echo "Error uploading files.";
}
?>
