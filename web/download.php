<?php
$jobId = $_GET['job'] ?? '';
$fileType = $_GET['file'] ?? '';
$resultsDir = 'results/';

$files = array(
    'alerts' => $jobId . '_alerts.csv',
    'resolved_customers' => $jobId . '_resolved_customers.csv',
    'golden_entities' => $jobId . '_golden_entities.csv',
    'node_features' => $jobId . '_node_features.csv',
    'edge_features' => $jobId . '_edge_features.csv',
    'summary' => $jobId . '_summary.json'
);

if (isset($files[$fileType])) {
    $filePath = $resultsDir . $files[$fileType];
    if (file_exists($filePath)) {
        $ext = pathinfo($filePath, PATHINFO_EXTENSION);
        header('Content-Type: text/' . ($ext == 'json' ? 'json' : 'csv'));
        header('Content-Disposition: attachment; filename="' . $files[$fileType] . '"');
        header('Content-Length: ' . filesize($filePath));
        readfile($filePath);
        exit;
    }
}
header('Location: index.php');
?>
