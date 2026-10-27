<?php
// Generate sample CSV files
$customers = array(
    array('customer_id','name','dob','address','phone','email','ssn','zip','device_id','ip_address','location'),
    array('1','John A Smith','1980-01-01','123 Main St NY','555-123-4567','john.smith@gmail.com','123-45-6789','10001','DEV001','192.168.1.100','NY'),
    array('2','Jon Smith','1980-01-01','123 Main Street New York','5551234567','jsmith@gmail.com','123-45-6789','10001','DEV001','192.168.1.100','NY'),
    array('3','Jane Doe','1990-05-05','456 Oak Ave CA','555-999-8888','jane.doe@yahoo.com','987-65-4321','90210','DEV002','10.0.0.50','CA'),
    array('4','Robert Johnson','1975-03-15','789 Pine Rd TX','555-444-3333','robert.j@company.com','555-66-7777','77001','DEV003','172.16.0.10','TX'),
    array('5','Bob Johnson','1975-03-15','789 Pine Road TX','5554443333','bobj@gmail.com','555-66-7777','77001','DEV003','172.16.0.10','TX'),
);

$transactions = array(
    array('transaction_id','sender_id','receiver_id','amount','timestamp','channel','location','transaction_type'),
    array('101','1','3','9500','2024-01-01 10:00:00','wire','NY','transfer'),
    array('102','1','3','9400','2024-01-01 12:00:00','wire','NY','transfer'),
    array('103','1','3','9600','2024-01-01 14:00:00','wire','NY','transfer'),
    array('104','4','5','15000','2024-01-02 10:00:00','ach','TX','transfer'),
    array('105','5','4','14000','2024-01-02 10:30:00','ach','TX','transfer'),
);

// Create ZIP
$zip = new ZipArchive();
$filename = "FinCrime_Sample_Data.zip";
if ($zip->open($filename, ZipArchive::CREATE | ZipArchive::OVERWRITE) === TRUE) {
    // Add customers CSV
    $customersContent = '';
    foreach ($customers as $row) {
        $customersContent .= implode(',', $row) . "\n";
    }
    $zip->addFromString('customers_sample.csv', $customersContent);
    
    // Add transactions CSV
    $transactionsContent = '';
    foreach ($transactions as $row) {
        $transactionsContent .= implode(',', $row) . "\n";
    }
    $zip->addFromString('transactions_sample.csv', $transactionsContent);
    
    $zip->close();
    
    header('Content-Type: application/zip');
    header('Content-disposition: attachment; filename='.$filename);
    header('Content-Length: ' . filesize($filename));
    readfile($filename);
    unlink($filename);
    exit;
}
?>
