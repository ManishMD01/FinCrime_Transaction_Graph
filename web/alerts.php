<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AML Alerts - FinCrime Engine</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .card { box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1.5rem; }
        .header { background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 1.5rem 0; }
        .badge-CRITICAL { background-color: #6f42c1; }
        .badge-HIGH { background-color: #dc3545; }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h2><i class="fas fa-exclamation-triangle"></i> AML/Fraud Alerts</h2>
                    <p class="mb-0">Alerts from BigQuery aml_alerts table</p>
                </div>
                <div>
                    <a href="index.php" class="btn btn-light"><i class="fas fa-home"></i> Dashboard</a>
                </div>
            </div>
        </div>
    </div>

    <div class="container mt-4">
        <div class="card">
            <div class="card-header bg-danger text-white d-flex justify-content-between align-items-center">
                <h5 class="mb-0"><i class="fas fa-bell"></i> Alerts</h5>
                <button class="btn btn-light btn-sm" onclick="loadAlerts()"><i class="fas fa-sync"></i> Refresh</button>
            </div>
            <div class="card-body">
                <div id="alertsContent">Loading...</div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    function loadAlerts() {
        fetch('alerts_api.php')
            .then(r => r.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('alertsContent').innerHTML = '<div class="alert alert-danger">' + data.error + '</div>';
                    return;
                }
                if (data.length == 0) {
                    document.getElementById('alertsContent').innerHTML = '<p class="text-muted">No alerts found. Run ETL and detection pipeline.</p>';
                    return;
                }
                let html = '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>Alert ID</th><th>Type</th><th>Severity</th><th>Golden Entity</th><th>Description</th><th>Date</th><th>Status</th></tr></thead><tbody>';
                data.forEach(a => {
                    html += '<tr><td>' + (a.alert_id||'') + '</td><td>' + (a.alert_type||'') + '</td><td><span class="badge badge-' + (a.severity||'') + '">' + (a.severity||'') + '</span></td><td>' + (a.golden_entity_id||'') + '</td><td>' + (a.description||'') + '</td><td>' + (a.alert_date||'') + '</td><td>' + (a.status||'') + '</td></tr>';
                });
                html += '</tbody></table></div>';
                document.getElementById('alertsContent').innerHTML = html;
            });
    }
    loadAlerts();
    </script>
</body>
</html>
