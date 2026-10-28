<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinCrime Entity Resolution - BigQuery Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1.5rem; }
        .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem 0; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h1><i class="fas fa-database"></i> FinCrime Entity Resolution - BigQuery</h1>
                    <p class="mb-0">AML & Fraud Detection from BigQuery Data</p>
                </div>
                <a href="search.php" class="btn btn-light btn-lg">
                    <i class="fas fa-search"></i> Search Customer / Transaction / Alert
                </a>
            </div>
        </div>
    </div>

    <div class="container mt-4">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-search"></i> Search Customer / Transaction / Alert ID</h5>
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

        <div class="row">
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-database fa-3x text-primary mb-3"></i>
                        <h5>Data from BigQuery</h5>
                        <p class="text-muted">Uses raw_customers and raw_transactions from BigQuery</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-link fa-3x text-success mb-3"></i>
                        <h5>Entity Resolution</h5>
                        <p class="text-muted">Resolves profiles and creates golden entities</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
                        <h5>Fraud Detection</h5>
                        <p class="text-muted">Detects smurfing, money mules, phantom profiles</p>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <div class="container mt-4 mb-4">
        <div class="card">
            <div class="card-header bg-danger text-white">
                <h5 class="mb-0"><i class="fas fa-exclamation-triangle"></i> AML Alerts Dashboard</h5>
            </div>
            <div class="card-body text-center">
                <p>View all AML/Fraud alerts from BigQuery</p>
                <a href="alerts.php" class="btn btn-danger btn-lg">
                    <i class="fas fa-bell"></i> View Alerts
                </a>
            </div>
        </div>
    </div>

    <footer class="py-3 bg-dark text-white text-center">
        <div class="container">
            <small>FinCrime Entity Resolution Engine - BigQuery Mode</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
