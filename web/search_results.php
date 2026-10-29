<?php
session_start();

$searchType = isset($_GET['search_type']) ? $_GET['search_type'] : '';
$searchTerm = isset($_GET['search_term']) ? $_GET['search_term'] : '';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results - FinCrime Engine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1.5rem; }
        .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 1.5rem 0; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h2><i class="fas fa-search-plus"></i> Search Results</h2>
                    <p class="mb-0">Search: <?php echo htmlspecialchars($searchType); ?> = <?php echo htmlspecialchars($searchTerm); ?></p>
                </div>
                <div>
                    <a href="search.php" class="btn btn-light"><i class="fas fa-arrow-left"></i> New Search</a>
                    <a href="index.php" class="btn btn-light"><i class="fas fa-home"></i> Dashboard</a>
                </div>
            </div>
        </div>
    </div>

    <div class="container mt-4">
        <?php
        $cmd = "cd /home/pritsingh000/Git/FinCrime_Transaction_Graph && GOOGLE_APPLICATION_CREDENTIALS='' PYTHONPATH=/home/pritsingh000/Git/FinCrime_Transaction_Graph:/home/pritsingh000/Git/FinCrime_Transaction_Graph/src:/home/pritsingh000/Git/FinCrime_Transaction_Graph/bigquery /home/pritsingh000/Git/FinCrime_Transaction_Graph/venv/bin/python web/search_query.py " . escapeshellarg($searchType) . " " . escapeshellarg($searchTerm);
        $output = array();
        $ret = 0;
        exec($cmd . ' 2>&1', $output, $ret);
        $jsonOut = trim(implode("\n", $output));
        // Remove warnings if any
        $lines = explode("\n", $jsonOut);
        $jsonLine = end($lines);
        while ($jsonLine !== false && (trim($jsonLine) === '' || trim($jsonLine)[0] !== '{' && trim($jsonLine)[0] !== '[')) {
            array_pop($lines);
            $jsonLine = end($lines);
        }
        if ($jsonLine && (trim($jsonLine)[0] === '{' || trim($jsonLine)[0] === '[')) {
            $jsonOut = trim($jsonLine);
        }
        $data = json_decode($jsonOut, true);
        
        if (!$data || isset($data['error'])) {
            echo '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> ' . (isset($data['error']) ? htmlspecialchars($data['error']) : 'No data found or error occurred') . '</div>';
            echo '<pre>' . htmlspecialchars($jsonOut) . '</pre>';
        } else {
            if (isset($data['customers']) && is_array($data['customers']) && count($data['customers']) > 0) {
                echo '<div class="card"><div class="card-header bg-success text-white"><h5 class="mb-0"><i class="fas fa-user"></i> Customer Details</h5></div><div class="card-body"><div class="table-responsive"><table class="table table-striped table-sm">';
                echo '<thead><tr><th>Customer ID</th><th>Name</th><th>DOB</th><th>Phone</th><th>Email</th><th>SSN</th><th>Address</th><th>Device ID</th><th>IP Address</th><th>Location</th></tr></thead><tbody>';
                foreach ($data['customers'] as $c) {
                    echo '<tr>';
                    echo '<td>' . (isset($c['customer_id']) ? htmlspecialchars($c['customer_id']) : '') . '</td>';
                    echo '<td>' . (isset($c['name']) ? htmlspecialchars($c['name']) : '') . '</td>';
                    echo '<td>' . (isset($c['dob']) ? htmlspecialchars($c['dob']) : '') . '</td>';
                    echo '<td>' . (isset($c['phone']) ? htmlspecialchars($c['phone']) : '') . '</td>';
                    echo '<td>' . (isset($c['email']) ? htmlspecialchars($c['email']) : '') . '</td>';
                    echo '<td>' . (isset($c['ssn']) ? htmlspecialchars($c['ssn']) : '') . '</td>';
                    echo '<td>' . (isset($c['address']) ? htmlspecialchars($c['address']) : '') . '</td>';
                    echo '<td>' . (isset($c['device_id']) ? htmlspecialchars($c['device_id']) : '') . '</td>';
                    echo '<td>' . (isset($c['ip_address']) ? htmlspecialchars($c['ip_address']) : '') . '</td>';
                    echo '<td>' . (isset($c['location']) ? htmlspecialchars($c['location']) : '') . '</td>';
                    echo '</tr>';
                }
                echo '</tbody></table></div></div></div>';
            }
            
            if (isset($data['transactions']) && is_array($data['transactions']) && count($data['transactions']) > 0) {
                echo '<div class="card"><div class="card-header bg-warning text-dark"><h5 class="mb-0"><i class="fas fa-exchange-alt"></i> All Transactions (Sent & Received) - ' . count($data['transactions']) . ' transactions</h5></div><div class="card-body"><div class="table-responsive"><table class="table table-striped table-sm">';
                echo '<thead><tr><th>Transaction ID</th><th>Sender ID</th><th>Receiver ID</th><th>Amount</th><th>Timestamp</th><th>Channel</th><th>Type</th><th>Location</th></tr></thead><tbody>';
                foreach ($data['transactions'] as $t) {
                    echo '<tr>';
                    echo '<td>' . (isset($t['transaction_id']) ? htmlspecialchars($t['transaction_id']) : '') . '</td>';
                    echo '<td>' . (isset($t['sender_id']) ? htmlspecialchars($t['sender_id']) : '') . '</td>';
                    echo '<td>' . (isset($t['receiver_id']) ? htmlspecialchars($t['receiver_id']) : '') . '</td>';
                    echo '<td>$' . (isset($t['amount']) ? htmlspecialchars($t['amount']) : '') . '</td>';
                    echo '<td>' . (isset($t['timestamp']) ? htmlspecialchars($t['timestamp']) : '') . '</td>';
                    echo '<td>' . (isset($t['channel']) ? htmlspecialchars($t['channel']) : '') . '</td>';
                    echo '<td>' . (isset($t['transaction_type']) ? htmlspecialchars($t['transaction_type']) : '') . '</td>';
                    echo '<td>' . (isset($t['location']) ? htmlspecialchars($t['location']) : '') . '</td>';
                    echo '</tr>';
                }
                echo '</tbody></table></div></div></div>';
            } elseif (isset($data['customers'])) {
                echo '<div class="alert alert-info">No transactions found for this customer.</div>';
            }
        }
        ?>
    </div>

    <footer class="mt-5 py-3 bg-dark text-white text-center">
        <div class="container">
            <small>FinCrime Entity Resolution Engine</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>


        <?php if (isset($data['transactions']) && is_array($data['transactions']) && count($data['transactions']) > 0 && isset($data['customers']) && count($data['customers']) > 0): ?>
        <div class="card">
            <div class="card-header bg-dark text-white">
                <h5 class="mb-0"><i class="fas fa-project-diagram"></i> Transaction Linking Graph - Debtor & Creditor Network</h5>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-6">
                        <h6 class="text-primary"><i class="fas fa-arrow-up"></i> Debtor (Sent From) - Outgoing Transactions</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-bordered">
                                <thead class="table-danger">
                                    <tr><th>To (Creditor)</th><th>Amount</th><th>Txn ID</th><th>Date</th></tr>
                                </thead>
                                <tbody>
                                    <?php 
                                    $custId = $data['customers'][0]['customer_id'];
                                    foreach ($data['transactions'] as $t) {
                                        if (isset($t['sender_id']) && (string)$t['sender_id'] === (string)$custId) {
                                            echo '<tr>';
                                            echo '<td><strong>' . htmlspecialchars($t['receiver_id']) . '</strong></td>';
                                            echo '<td>$' . htmlspecialchars($t['amount']) . '</td>';
                                            echo '<td>' . htmlspecialchars($t['transaction_id']) . '</td>';
                                            echo '<td>' . htmlspecialchars($t['timestamp']) . '</td>';
                                            echo '</tr>';
                                        }
                                    }
                                    ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-success"><i class="fas fa-arrow-down"></i> Creditor (Received To) - Incoming Transactions</h6>
                        <div class="table-responsive">
                            <table class="table table-sm table-bordered">
                                <thead class="table-success">
                                    <tr><th>From (Debtor)</th><th>Amount</th><th>Txn ID</th><th>Date</th></tr>
                                </thead>
                                <tbody>
                                    <?php 
                                    foreach ($data['transactions'] as $t) {
                                        if (isset($t['receiver_id']) && (string)$t['receiver_id'] === (string)$custId) {
                                            echo '<tr>';
                                            echo '<td><strong>' . htmlspecialchars($t['sender_id']) . '</strong></td>';
                                            echo '<td>$' . htmlspecialchars($t['amount']) . '</td>';
                                            echo '<td>' . htmlspecialchars($t['transaction_id']) . '</td>';
                                            echo '<td>' . htmlspecialchars($t['timestamp']) . '</td>';
                                            echo '</tr>';
                                        }
                                    }
                                    ?>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="alert alert-info">
                    <strong>Transaction Linkage Summary:</strong> 
                    <?php 
                    $sent = 0; $recv = 0;
                    foreach ($data['transactions'] as $t) {
                        if (isset($t['sender_id']) && (string)$t['sender_id'] === (string)$custId) $sent++;
                        if (isset($t['receiver_id']) && (string)$t['receiver_id'] === (string)$custId) $recv++;
                    }
                    echo "Sent: $sent transactions | Received: $recv transactions | Total Linked: " . count($data['transactions']);
                    ?>
                </div>
            </div>
        </div>
        <?php endif; ?>


        <?php if (isset($data['transactions']) && is_array($data['transactions']) && count($data['transactions']) > 0 && isset($data['customers']) && count($data['customers']) > 0): ?>
        <div class="card">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="fas fa-share-alt"></i> Neural Network Transaction Graph</h5>
            </div>
            <div class="card-body">
                <div id="networkGraph" style="width: 100%; height: 500px; border: 1px solid #ddd; background: #fafafa;"></div>
                <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                    if (typeof vis === 'undefined') { document.getElementById('networkGraph').innerHTML = 'Graph library failed to load'; return; }
                    var nodes = new vis.DataSet([
                        {id: '<?php echo $custId; ?>', label: 'Customer\n<?php echo $custId; ?>', color: '#ff6b6b', shape: 'dot', size: 30}
                    ]);
                    var edges = new vis.DataSet([]);
                    <?php 
                    $addedNodes = array($custId => true);
                    foreach ($data['transactions'] as $t) {
                        if (isset($t['sender_id']) && (string)$t['sender_id'] !== (string)$custId) {
                            $s = htmlspecialchars($t['sender_id']);
                            $a = htmlspecialchars($t['amount']);
                            if (!isset($addedNodes[$s])) {
                                echo "nodes.add({id: '$s', label: 'Debtor\n$s', color: '#4dabf7', shape: 'dot', size: 25});\n";
                                $addedNodes[$s] = true;
                            }
                            echo "edges.add({from: '$s', to: '$custId', label: '\$$a', arrows: 'to'});\n";
                        }
                        if (isset($t['receiver_id']) && (string)$t['receiver_id'] !== (string)$custId) {
                            $r = htmlspecialchars($t['receiver_id']);
                            $a = htmlspecialchars($t['amount']);
                            if (!isset($addedNodes[$r])) {
                                echo "nodes.add({id: '$r', label: 'Creditor\n$r', color: '#51cf66', shape: 'dot', size: 25});\n";
                                $addedNodes[$r] = true;
                            }
                            echo "edges.add({from: '$custId', to: '$r', label: '\$$a', arrows: 'to'});\n";
                        }
                    }
                    ?>
                    var container = document.getElementById('networkGraph');
                    var data = {nodes: nodes, edges: edges};
                    var options = {
                        layout: {hierarchical: false},
                        physics: {enabled: true, barnesHut: {gravitationalConstant: -2000}},
                        nodes: {font: {size: 12}},
                        edges: {font: {size: 10, align: 'middle'}}
                    };
                    new vis.Network(container, data, options);
                    });
                </script>
            </div>
        </div>
        <?php endif; ?>

        <script>
        window.onload = function() {
            if (typeof vis !== 'undefined') {
                console.log('vis loaded');
            } else {
                console.log('vis not loaded');
            }
        };
        </script>
