<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinCrime Entity Resolution & Transaction Graph Engine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1.5rem; }
        .header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 2rem 0; }
        .nav-tabs .nav-link.active { background-color: #2a5298; color: white; border-color: #2a5298; }
        .badge-high { background-color: #dc3545; }
        .badge-critical { background-color: #6f42c1; }
        .badge-medium { background-color: #fd7e14; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1><i class="fas fa-shield-alt"></i> FinCrime Entity Resolution Engine</h1>
            <p class="mb-0">AML & Fraud Detection | Entity Resolution | Transaction Graph Analytics</p>
        </div>
    </div>

    <div class="container mt-4">
        <!-- Upload Section -->
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-upload"></i> Data Upload</h5>
            </div>
            <div class="card-body">
                <form action="process.php" method="POST" enctype="multipart/form-data">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="customers" class="form-label"><strong>Customer Profiles CSV</strong></label>
                                <input type="file" class="form-control" id="customers" name="customers" accept=".csv" required>
                                <small class="text-muted">Required: customer_id, name, dob, address, phone, email, ssn, zip, device_id, ip_address, location</small>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="transactions" class="form-label"><strong>Transaction Logs CSV</strong></label>
                                <input type="file" class="form-control" id="transactions" name="transactions" accept=".csv" required>
                                <small class="text-muted">Required: transaction_id, sender_id, receiver_id, amount, timestamp, channel, location, transaction_type</small>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label for="threshold" class="form-label">Match Threshold</label>
                                <input type="range" class="form-range" id="threshold" name="threshold" min="0.5" max="0.95" step="0.05" value="0.75" oninput="thresholdValue.value = threshold.value">
                                <output id="thresholdValue">0.75</output>
                            </div>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg">
                        <i class="fas fa-play"></i> Run Entity Resolution & Detection
                    </button>
                    <a href="sample.php" class="btn btn-outline-secondary btn-lg">
                        <i class="fas fa-download"></i> Download Sample Data
                    </a>
                </form>
            </div>
        </div>

        <!-- Features Overview -->
        <div class="row">
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-link fa-3x text-primary mb-3"></i>
                        <h5>Entity Resolution</h5>
                        <p class="text-muted">Connect disjointed profiles using fuzzy matching & graph clustering</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-project-diagram fa-3x text-success mb-3"></i>
                        <h5>Transaction Graph</h5>
                        <p class="text-muted">Build unified customer-transaction graphs with rich features</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center">
                    <div class="card-body">
                        <i class="fas fa-exclamation-triangle fa-3x text-danger mb-3"></i>
                        <h5>AML/Fraud Detection</h5>
                        <p class="text-muted">Detect structuring, money mules, and phantom profiles</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Documentation -->
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0"><i class="fas fa-book"></i> Detection Capabilities</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <h6><span class="badge badge-high">HIGH</span> Structuring/Smurfing</h6>
                        <p class="small">Multiple transactions just below $10,000 reporting threshold in short time windows</p>
                    </div>
                    <div class="col-md-4">
                        <h6><span class="badge badge-critical">CRITICAL</span> Money Mule Networks</h6>
                        <p class="small">Funds from multiple sources rapidly transferred to external entities</p>
                    </div>
                    <div class="col-md-4">
                        <h6><span class="badge badge-high">HIGH</span> Rapid Velocity/Phantom Profiles</h6>
                        <p class="small">Multiple profiles (same entity) with high-frequency txns from same device/IP</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="mt-5 py-3 bg-dark text-white text-center">
        <div class="container">
            <small>FinCrime Entity Resolution Engine - For Compliance & Investigation Purposes</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
