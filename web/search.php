<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Search - FinCrime Engine</title>
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
                    <h2><i class="fas fa-search"></i> Search Customer / Transaction / Alert</h2>
                    <p class="mb-0">View full transaction linkage, sent/received transactions & entity details</p>
                </div>
                <div>
                    <a href="index.php" class="btn btn-light"><i class="fas fa-home"></i> Dashboard</a>
                    <a href="results.php?job_id=<?php echo $_SESSION['job_id'] ?? ''; ?>" class="btn btn-light"><i class="fas fa-chart-line"></i> Results</a>
                </div>
            </div>
        </div>
    </div>

    <div class="container mt-4">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-filter"></i> Search</h5>
            </div>
            <div class="card-body">
                <form action="search_results.php" method="GET">
                    <div class="row">
                        <div class="col-md-3">
                            <div class="mb-3">
                                <label for="search_type" class="form-label"><strong>Search By</strong></label>
                                <select class="form-select" id="search_type" name="search_type" required>
                                    <option value="customer_id">Customer ID</option>
                                    <option value="transaction_id">Transaction ID</option>
                                    <option value="alert_id">Alert ID</option>
                                    <option value="golden_entity_id">Golden Entity ID</option>
                                    <option value="name">Customer Name</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-7">
                            <div class="mb-3">
                                <label for="search_term" class="form-label"><strong>Search Term</strong></label>
                                <input type="text" class="form-control" id="search_term" name="search_term" placeholder="Enter ID or Name..." required>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="mb-3">
                                <label class="form-label">&nbsp;</label>
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="fas fa-search"></i> Search
                                </button>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
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
