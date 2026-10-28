<?php
session_start();
$jobId = $_SESSION['job_id'] ?? '';
$resultsDir = 'results/';

$searchType = $_GET['search_type'] ?? '';
$searchTerm = $_GET['search_term'] ?? '';

function readCSV($file) {
    if (!file_exists($file)) return [];
    $rows = array();
    if (($handle = fopen($file, "r")) !== FALSE) {
        $header = fgetcsv($handle);
        while (($data = fgetcsv($handle)) !== FALSE) {
            if (count($header) == count($data)) {
                $rows[] = array_combine($header, $data);
            }
        }
        fclose($handle);
    }
    return $rows;
}

$resolved = readCSV($resultsDir . $jobId . '_resolved_customers.csv');
$golden = readCSV($resultsDir . $jobId . '_golden_entities.csv');
$alerts = readCSV($resultsDir . $jobId . '_alerts.csv');

// This would need actual transaction data - for demo using session
$transactions = array(); // Would load from BigQuery results
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
        <div class="card">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="fas fa-user"></i> Customer / Entity Details</h5>
            </div>
            <div class="card-body">
                <p class="text-muted">Search functionality requires transaction data from BigQuery. Run detection from BigQuery first to populate results.</p>
                <p>Search Type: <strong><?php echo htmlspecialchars($searchType); ?></strong> | Term: <strong><?php echo htmlspecialchars($searchTerm); ?></strong></p>
            </div>
        </div>

        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> To view full transaction linkage graphs and sent/received transactions, ensure data is loaded from BigQuery and detection has been run.
        </div>
    </div>

    <footer class="mt-5 py-3 bg-dark text-white text-center">
        <div class="container">
            <small>FinCrime Entity Resolution Engine</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
