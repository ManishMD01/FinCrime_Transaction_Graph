<?php
session_start();
$jobId = $_GET['job_id'] ?? $_SESSION['job_id'] ?? '';
$resultsDir = 'results/';

$summaryFile = $resultsDir . $jobId . '_summary.json';
if (!file_exists($summaryFile)) {
    header('Location: index.php');
    exit;
}

$summary = json_decode(file_get_contents($summaryFile), true);

function readCSV($file) {
    if (!file_exists($file)) return [];
    $rows = array();
    if (($handle = fopen($file, "r")) !== FALSE) {
        $header = fgetcsv($handle);
        while (($data = fgetcsv($handle)) !== FALSE) {
            $rows[] = array_combine($header, $data);
        }
        fclose($handle);
    }
    return $rows;
}

$alerts = readCSV($resultsDir . $jobId . '_alerts.csv');
$resolved = readCSV($resultsDir . $jobId . '_resolved_customers.csv');
$golden = readCSV($resultsDir . $jobId . '_golden_entities.csv');
$nodeFeatures = readCSV($resultsDir . $jobId . '_node_features.csv');
$edgeFeatures = readCSV($resultsDir . $jobId . '_edge_features.csv');
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Results - FinCrime Engine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1.5rem; }
        .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 1.5rem 0; }
        .stat-card { text-align: center; padding: 1rem; }
        .stat-number { font-size: 2rem; font-weight: bold; }
        .badge-CRITICAL { background-color: #6f42c1; }
        .badge-HIGH { background-color: #dc3545; }
        .badge-MEDIUM { background-color: #fd7e14; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h2><i class="fas fa-chart-line"></i> Analysis Results</h2>
                    <p class="mb-0">Job ID: <?php echo htmlspecialchars($jobId); ?></p>
                </div>
                <a href="index.php" class="btn btn-light"><i class="fas fa-home"></i> New Analysis</a>
            </div>
        </div>
    </div>

    <div class="container mt-4">
        <?php if ($summary['status'] === 'error'): ?>
            <div class="alert alert-danger">
                <h4><i class="fas fa-exclamation-circle"></i> Error</h4>
                <p><?php echo htmlspecialchars($summary['error']); ?></p>
            </div>
        <?php else: ?>
            <!-- Summary Stats -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="stat-number text-primary"><?php echo $summary['total_customers']; ?></div>
                        <div class="text-muted">Input Customers</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="stat-number text-success"><?php echo $summary['golden_entities']; ?></div>
                        <div class="text-muted">Golden Entities</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="stat-number text-info"><?php echo $summary['total_transactions']; ?></div>
                        <div class="text-muted">Transactions</div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card stat-card">
                        <div class="stat-number text-danger"><?php echo $summary['total_alerts']; ?></div>
                        <div class="text-muted">Alerts Generated</div>
                    </div>
                </div>
            </div>

            <!-- Pipeline Performance -->
            <div class="card">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0"><i class="fas fa-tachometer-alt"></i> Pipeline Performance</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <strong>Blocking Efficiency:</strong><br>
                            Candidate Pairs: <?php echo $summary['blocking_stats']['candidate_pairs'] ?? 'N/A'; ?><br>
                            Reduction: <?php echo $summary['blocking_stats']['reduction_percentage'] ?? 'N/A'; ?>
                        </div>
                        <div class="col-md-6">
                            <strong>Clustering:</strong><br>
                            Clusters with matches: <?php echo $summary['clustering_stats']['clusters_with_matches'] ?? 'N/A'; ?><br>
                            Largest cluster: <?php echo $summary['clustering_stats']['largest_cluster_size'] ?? 'N/A'; ?> members
                        </div>
                    </div>
                </div>
            </div>

            <!-- Alerts -->
            <div class="card">
                <div class="card-header bg-danger text-white">
                    <h5 class="mb-0"><i class="fas fa-exclamation-triangle"></i> AML/Fraud Alerts (<?php echo count($alerts); ?>)</h5>
                </div>
                <div class="card-body">
                    <?php if (count($alerts) == 0): ?>
                        <p class="text-muted">No suspicious patterns detected.</p>
                    <?php else: ?>
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>Alert Type</th>
                                        <th>Severity</th>
                                        <th>Golden Entity ID</th>
                                        <th>Description</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($alerts as $alert): ?>
                                    <tr>
                                        <td><?php echo htmlspecialchars($alert['alert_type']); ?></td>
                                        <td><span class="badge badge-<?php echo $alert['severity']; ?>"><?php echo $alert['severity']; ?></span></td>
                                        <td><?php echo htmlspecialchars($alert['golden_entity_id']); ?></td>
                                        <td><?php echo htmlspecialchars($alert['description']); ?></td>
                                    </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                    <?php endif; ?>
                </div>
            </div>

            <!-- Tabs for detailed results -->
            <ul class="nav nav-tabs" id="resultTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="golden-tab" data-bs-toggle="tab" data-bs-target="#golden" type="button">Golden Entities</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="resolved-tab" data-bs-toggle="tab" data-bs-target="#resolved" type="button">Resolved Customers</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="features-tab" data-bs-toggle="tab" data-bs-target="#features" type="button">Node Features</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="edges-tab" data-bs-toggle="tab" data-bs-target="#edges" type="button">Edge Features</button>
                </li>
            </ul>
            <div class="tab-content" id="resultTabsContent">
                <div class="tab-pane fade show active" id="golden" role="tabpanel">
                    <div class="card">
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Golden Entity ID</th>
                                            <th>Members</th>
                                            <th>Primary Name</th>
                                            <th>Primary Phone</th>
                                            <th>Primary Email</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($golden as $g): ?>
                                        <tr>
                                            <td><?php echo htmlspecialchars($g['golden_entity_id']); ?></td>
                                            <td><?php echo htmlspecialchars($g['member_count']); ?></td>
                                            <td><?php echo htmlspecialchars($g['primary_name']); ?></td>
                                            <td><?php echo htmlspecialchars($g['primary_phone']); ?></td>
                                            <td><?php echo htmlspecialchars($g['primary_email']); ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="resolved" role="tabpanel">
                    <div class="card">
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Customer ID</th>
                                            <th>Name</th>
                                            <th>Golden Entity ID</th>
                                            <th>Phone</th>
                                            <th>Email</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($resolved as $r): ?>
                                        <tr>
                                            <td><?php echo htmlspecialchars($r['customer_id']); ?></td>
                                            <td><?php echo htmlspecialchars($r['full_name_clean']); ?></td>
                                            <td><span class="badge bg-primary"><?php echo htmlspecialchars($r['golden_entity_id']); ?></span></td>
                                            <td><?php echo htmlspecialchars($r['phone_std']); ?></td>
                                            <td><?php echo htmlspecialchars($r['email_std']); ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="features" role="tabpanel">
                    <div class="card">
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>Entity ID</th>
                                            <th>Total Volume</th>
                                            <th>Inflow</th>
                                            <th>Outflow</th>
                                            <th>Freq</th>
                                            <th>Velocity (txns/hr)</th>
                                            <th>Counterparties</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($nodeFeatures as $nf): ?>
                                        <tr>
                                            <td><?php echo htmlspecialchars($nf['golden_entity_id']); ?></td>
                                            <td>$<?php echo number_format($nf['total_volume'], 2); ?></td>
                                            <td>$<?php echo number_format($nf['total_inflow'], 2); ?></td>
                                            <td>$<?php echo number_format($nf['total_outflow'], 2); ?></td>
                                            <td><?php echo htmlspecialchars($nf['transaction_frequency']); ?></td>
                                            <td><?php echo number_format($nf['velocity_txns_per_hour'], 2); ?></td>
                                            <td><?php echo htmlspecialchars($nf['unique_counterparties']); ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="tab-pane fade" id="edges" role="tabpanel">
                    <div class="card">
                        <div class="card-body">
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>From Entity</th>
                                            <th>To Entity</th>
                                            <th>Total Amount</th>
                                            <th>Count</th>
                                            <th>Avg Amount</th>
                                            <th>Cross-Border</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($edgeFeatures as $ef): ?>
                                        <tr>
                                            <td><?php echo htmlspecialchars($ef['sender_entity']); ?></td>
                                            <td><?php echo htmlspecialchars($ef['receiver_entity']); ?></td>
                                            <td>$<?php echo number_format($ef['total_amount'], 2); ?></td>
                                            <td><?php echo htmlspecialchars($ef['transaction_count']); ?></td>
                                            <td>$<?php echo number_format($ef['avg_amount'], 2); ?></td>
                                            <td><?php echo $ef['cross_border'] == 'True' ? '<span class="badge bg-warning">Yes</span>' : 'No'; ?></td>
                                        </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Downloads -->
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0"><i class="fas fa-download"></i> Download Results</h5>
                </div>
                <div class="card-body">
                    <a href="download.php?job=<?php echo $jobId; ?>&file=alerts" class="btn btn-outline-danger">Alerts CSV</a>
                    <a href="download.php?job=<?php echo $jobId; ?>&file=resolved_customers" class="btn btn-outline-primary">Resolved Customers CSV</a>
                    <a href="download.php?job=<?php echo $jobId; ?>&file=golden_entities" class="btn btn-outline-success">Golden Entities CSV</a>
                    <a href="download.php?job=<?php echo $jobId; ?>&file=node_features" class="btn btn-outline-info">Node Features CSV</a>
                    <a href="download.php?job=<?php echo $jobId; ?>&file=edge_features" class="btn btn-outline-secondary">Edge Features CSV</a>
                    <a href="download.php?job=<?php echo $jobId; ?>&file=summary" class="btn btn-outline-dark">Summary JSON</a>
                </div>
            </div>
        <?php endif; ?>
    </div>

    <footer class="mt-5 py-3 bg-dark text-white text-center">
        <div class="container">
            <small>FinCrime Entity Resolution Engine</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
