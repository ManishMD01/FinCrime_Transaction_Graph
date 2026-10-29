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
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1.5rem; }
        .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 1.5rem 0; }
        #networkGraph { width: 100%; height: 500px; border: 1px solid #ccc; }
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
        exec($cmd . ' 2>&1', $output);
        $jsonOut = trim(implode("\n", $output));
        $lines = explode("\n", $jsonOut);
        $jsonLine = end($lines);
        while ($jsonLine !== false && trim($jsonLine) !== '' && strlen($jsonLine) > 0 && $jsonLine[0] !== '{' && $jsonLine[0] !== '[') {
            array_pop($lines);
            $jsonLine = end($lines);
        }
        if ($jsonLine && strlen(trim($jsonLine)) > 0 && (trim($jsonLine)[0] === '{' || trim($jsonLine)[0] === '[')) {
            $jsonOut = trim($jsonLine);
        }
        $data = json_decode($jsonOut, true);
        
        if (isset($data['customers']) && is_array($data['customers']) && count($data['customers']) > 0) {
            echo '<div class="card"><div class="card-header bg-success text-white"><h5 class="mb-0"><i class="fas fa-user"></i> Customer Details</h5></div><div class="card-body"><div class="table-responsive"><table class="table table-striped table-sm">';
            echo '<thead><tr><th>Customer ID</th><th>Name</th><th>Phone</th><th>Email</th><th>Location</th></tr></thead><tbody>';
            foreach ($data['customers'] as $c) {
                echo '<tr><td>' . htmlspecialchars($c['customer_id']??'') . '</td><td>' . htmlspecialchars($c['name']??'') . '</td><td>' . htmlspecialchars($c['phone']??'') . '</td><td>' . htmlspecialchars($c['email']??'') . '</td><td>' . htmlspecialchars($c['location']??'') . '</td></tr>';
            }
            echo '</tbody></table></div></div></div>';
        }
        
        if (isset($data['transactions']) && is_array($data['transactions']) && count($data['transactions']) > 0 && isset($data['customers']) && count($data['customers']) > 0) {
            $custId = $data['customers'][0]['customer_id'];
            echo '<div class="card"><div class="card-header bg-warning text-dark"><h5 class="mb-0"><i class="fas fa-exchange-alt"></i> Transactions</h5></div><div class="card-body"><div class="table-responsive"><table class="table table-striped table-sm">';
            echo '<thead><tr><th>Txn ID</th><th>From</th><th>To</th><th>Amount</th><th>Date</th></tr></thead><tbody>';
            foreach ($data['transactions'] as $t) {
                echo '<tr><td>' . htmlspecialchars($t['transaction_id']??'') . '</td><td>' . htmlspecialchars($t['sender_id']??'') . '</td><td>' . htmlspecialchars($t['receiver_id']??'') . '</td><td>$' . htmlspecialchars($t['amount']??'') . '</td><td>' . htmlspecialchars($t['timestamp']??'') . '</td></tr>';
            }
            echo '</tbody></table></div></div></div>';
            
            echo '<div class="card"><div class="card-header bg-info text-white"><h5 class="mb-0"><i class="fas fa-project-diagram"></i> Entity Relation Graph</h5></div><div class="card-body"><div id="networkGraph"></div><div class="mt-3 text-center"><span style="color:#ff4757;">&#9472;&#9472; Red = Outgoing (Sent)</span> &nbsp;&nbsp; <span style="color:#1e90ff;">&#9472;&#9472; Blue = Incoming (Received)</span> &nbsp;&nbsp; <span style="color:#2ed573;">&#9679; Green = Creditor</span> &nbsp;&nbsp; <span style="color:#1e90ff;">&#9679; Blue = Debtor</span> &nbsp;&nbsp; <span style="color:#ff4757;">&#9679; Red = Current Customer</span></div></div></div>';
            echo '<script>
            var nodes = new vis.DataSet([{id:"' . $custId . '", label:"Customer\n' . $custId . '", color:"#ff4757", size:30}]);
            var edges = new vis.DataSet([]);
            ';
            $added = array($custId => true);
            foreach ($data['transactions'] as $t) {
                if (isset($t['sender_id']) && (string)$t['sender_id'] != (string)$custId) {
                    $s = $t['sender_id'];
                    if (!isset($added[$s])) {
                        echo 'nodes.add({id:"' . $s . '", label:"' . $s . '", color:"#1e90ff", size:20});';
                        $added[$s] = true;
                    }
                    echo 'edges.add({from:"' . $s . '", to:"' . $custId . '", arrows:{to:{enabled:true}}, color:{color:"#1e90ff"}, title:"Txn: ' . $t['transaction_id'] . ' | Amount: $' . $t['amount'] . ' | Date: ' . $t['timestamp'] . '"});';
                }
                if (isset($t['receiver_id']) && (string)$t['receiver_id'] != (string)$custId) {
                    $r = $t['receiver_id'];
                    if (!isset($added[$r])) {
                        echo 'nodes.add({id:"' . $r . '", label:"' . $r . '", color:"#2ed573", size:20});';
                        $added[$r] = true;
                    }
                    echo 'edges.add({from:"' . $custId . '", to:"' . $r . '", arrows:{to:{enabled:true}}, color:{color:"#ff4757"}, title:"Txn: ' . $t['transaction_id'] . ' | Amount: $' . $t['amount'] . ' | Date: ' . $t['timestamp'] . '"});';
                }
            }
            echo '
            var container = document.getElementById("networkGraph");
            var data = {nodes: nodes, edges: edges};
            var options = {physics:{enabled:true, stabilization:true}, interaction:{hover:true}, edges:{smooth:true}};
            new vis.Network(container, data, options);
            </script>';
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
