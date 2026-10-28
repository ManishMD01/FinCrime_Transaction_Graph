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
            <h1><i class="fas fa-database"></i> FinCrime Entity Resolution - BigQuery</h1>
            <p class="mb-0">AML & Fraud Detection from BigQuery Data</p>
        </div>
    </div>

    <div class="container mt-4">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-search"></i> Run Detection on BigQuery Data</h5>
            </div>
            <div class="card-body">
                <form action="process_bq.php" method="POST">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="days_back" class="form-label"><strong>Historical Data Period</strong></label>
                                <select class="form-select" id="days_back" name="days_back">
                                    <option value="30">Last 30 Days</option>
                                    <option value="90">Last 90 Days</option>
                                    <option value="180">Last 180 Days</option>
                                    <option value="365" selected>Last 365 Days</option>
                                    <option value="all">All Historical Data</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="threshold" class="form-label">Match Threshold</label>
                                <input type="range" class="form-range" id="threshold" name="threshold" min="0.5" max="0.95" step="0.05" value="0.75" oninput="thresholdValue.value = threshold.value">
                                <output id="thresholdValue">0.75</output>
                            </div>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="fas fa-play"></i> Run Entity Resolution & Fraud Detection
                    </button>
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

    <footer class="mt-5 py-3 bg-dark text-white text-center">
        <div class="container">
            <small>FinCrime Entity Resolution Engine - BigQuery Mode</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>


        <div class="text-center mt-4">
            <a href="search.php" class="btn btn-outline-primary btn-lg">
                <i class="fas fa-search"></i> Search by Customer / Transaction / Alert ID
            </a>
        </div>
